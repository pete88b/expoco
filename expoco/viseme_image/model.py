# AUTOGENERATED! DO NOT EDIT! File to edit: 11d_viseme_image_model.ipynb (unless otherwise specified).

__all__ = ['prepare_for_inference', 'VisemeClassifier']

# Cell
from .data import *
from pathlib import Path
import numpy as np
import cv2, onnxruntime

# Cell
def prepare_for_inference(image, image_size=256):
    "Convert a cv2 style image to something that can be used as input to a CNN"
    if image.shape[0] > image_size:
        image = ImageHelper().face_crop(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.transpose(image, (2, 0, 1))
    image = (image/255.)
    image = image.astype(np.float32)
    return image

# Cell
class VisemeClassifier:
    def __init__(self, model_path, image_size=256):
        self.model = onnxruntime.InferenceSession(str(model_path))
        self.image_size = image_size
        self.image_helper = ImageHelper()
        self.vocab = ['AH', 'EE', 'NO_EXPRESSION', 'OO']
        self.item_queue = []
    def _to_image(self, item):
        return self.image_helper.read_image(item) if isinstance(item, (str, Path)) else item
    def predict(self, items=None):
        if items is None:
            items = self.item_queue
            self.item_queue = []
        else:
            items = [self._to_image(i) for i in items]
            items = [prepare_for_inference(i, self.image_size) for i in items]
        items = np.array(items)
        model_output = self.model.run(None, {'input': items})
        output = model_output[0]
        class_ids = np.argmax(output, axis=1)
        class_names = [self.vocab[class_id] for class_id in class_ids]
        return class_names
    def queue_item(self, item):
        self.item_queue.append(prepare_for_inference(self._to_image(item), self.image_size))