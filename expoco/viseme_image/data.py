# AUTOGENERATED! DO NOT EDIT! File to edit: 11b_viseme_image_data.ipynb (unless otherwise specified).

__all__ = ['mp_face_mesh', 'mp_face_detection', 'ImageHelper', 'viseme_image_dataset_from_capture_sessions',
           'calculate_stats', 'add_stats_to_metadata']

# Cell
from ..core import *
from ..camera_capture import *
import numpy as np
import cv2, time, math, json, tempfile, shutil, zlib

import mediapipe as mp
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection

from pathlib import Path
from zipfile import ZipFile

# Cell
class ImageHelper:
    def __init__(self):
        self.face_detection = mp_face_detection.FaceDetection()
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def read_image(self, file_name):
        assert Path(file_name).is_file(), f'Failed to read image. {file_name} not found'
        return cv2.imread(str(file_name))
    def write_image(self, file_name, image):
        return cv2.imwrite(str(file_name), image)
    def flip(self, image):
        return cv2.flip(image, 1)
    def get_face_bounding_box(self, image):
        def normalized_x_to_pixel(value):
            return math.floor(value * image.shape[1]) # width
        def normalized_y_to_pixel(value):
            return math.floor(value * image.shape[0]) # height
        results = self.face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.detections:
            return None
        relative_bbox = results.detections[0].location_data.relative_bounding_box
        xmin, width = [normalized_x_to_pixel(i) for i in [relative_bbox.xmin, relative_bbox.width]]
        ymin, height = [normalized_y_to_pixel(i) for i in [relative_bbox.ymin, relative_bbox.height]]
        return xmin, ymin, width, height
    def resize_face_bounding_box(self, bbox, size=256):
        xmin, ymin, width, height = bbox
        xmin -= ((size - width) // 2)
        ymin -= ((size - height) // 2)
        return xmin, ymin, size, size
    def face_crop(self, image, size=256):
        bbox = self.get_face_bounding_box(image)
        xmin, ymin, width, height = self.resize_face_bounding_box(bbox)
        return image[ymin:ymin+height, xmin:xmin+width]

# Cell
def _make_zip(dataset_path):
    default_compression=zlib.Z_DEFAULT_COMPRESSION
    try:
        zlib.Z_DEFAULT_COMPRESSION=0
        shutil.make_archive(dataset_path/'data', 'zip', dataset_path/'images')
    finally:
        zlib.Z_DEFAULT_COMPRESSION=default_compression

# Cell
def viseme_image_dataset_from_capture_sessions(
        input_path='data/capture_sessions',
        glob_pattern='*',
        change_y_from=None, change_y_to=None):
    "Create a viseme image dataset from capture session images"
    if change_y_from is not None: assert change_y_to is not None
    input_path, dataset_id, image_helper = Path(input_path), now(), ImageHelper()
    output_path = input_path.parent/f'viseme_image_dataset_{dataset_id}'
    output_path.mkdir()
    metadata = dict(input_path=path_to_str(input_path), output_path=path_to_str(output_path),
                    glob_pattern=glob_pattern, session_metadata=[], start_date=now(),
                    change_y_from=change_y_from, change_y_to=change_y_to,)
    for session_path in sorted(input_path.glob(glob_pattern)):
        with open(session_path/'metadata.json') as f:
            session_metadata = json.load(f)
        metadata['session_metadata'].append(session_metadata)
        viseme_class = get_viseme_class(session_metadata)
        if viseme_class == change_y_from:
            viseme_class = change_y_to
        for capture_count in range(1, session_metadata['count']+1):
            image = image_helper.read_image(session_path/f'{capture_count}.png')
            image = image_helper.face_crop(image)
            image_file_path = output_path/f'images/{viseme_class}/{session_path.name}_{capture_count}.png'
            image_file_path.parent.mkdir(parents=True, exist_ok=True)
            image_helper.write_image(image_file_path, image)
    _make_zip(output_path)
    metadata['end_date'] = now()
    with open(output_path/'metadata.json', 'w') as f: json.dump(metadata, f, indent=2)
    return output_path

# Cell
def calculate_stats(dataset_path, sample_fraction=0.1):
    "Color channel wise (BGR) mean and standard deviation"
    dataset_path = Path(dataset_path)
    image_helper, images = ImageHelper(), []
    for p in [p for p in (dataset_path/'images').iterdir() if p.is_dir()]:
        file_paths = [f for f in p.iterdir()]
        sample_size = round(len(file_paths) * sample_fraction)
        print(p, 'sample_size', sample_size)
        for f in np.random.choice(file_paths, sample_size, replace=False):
            images.append(image_helper.read_image(f))
    images = np.array(images) / 255.0
    return images.mean(axis=(0,1,2)), images.std(axis=(0,1,2))

# Cell
def add_stats_to_metadata(dataset_path, stats):
    with open(dataset_path/'metadata.json') as f:
        metadata = json.load(f)
    metadata['stats'] = dict(mean=np.round(stats[0], 4).tolist(), std=np.round(stats[1], 4).tolist())
    with open(dataset_path/'metadata.json', 'w') as f: json.dump(metadata, f, indent=2)