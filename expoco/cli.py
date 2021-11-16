# AUTOGENERATED! DO NOT EDIT! File to edit: 70_cli.ipynb (unless otherwise specified).

__all__ = ['dry_run', 'capture_session', 'capture_session2', 'viseme_dataset_from_capture_sessions',
           'processed_dataset_from_viseme_dataset']

# Cell
from .core import *
from .face_mesh.capture_session import capture_session as _capture_session
from .face_mesh.capture_session import dry_run as _dry_run
from .ml.data import viseme_dataset_from_capture_sessions as _viseme_dataset_from_capture_sessions
from .ml.data import processed_dataset_from_viseme_dataset as _processed_dataset_from_viseme_dataset
from fastcore.script import *

# Cell
@call_parse
def dry_run():
    _dry_run()

# Cell
@call_parse
def capture_session(expression_id:Param('', int),
                    stop_after:Param('', int),
                    comments:Param('', str)):
    path = _capture_session(expression_id, stop_after, comments)
    print('Capture session path', path)

# Cell
@call_parse # TODO: think of a better name
def capture_session2(stop_after:Param('', int),
                     comments:Param('', str)):
    import cv2
    window_name = 'expoco: Capture session'
    for k, v in dict(
            center_box=[(1280-640)//2, (720-480)//2],
            top_left_box=[0, 0],
            top_right_box=[1280-640, 0],
            bottom_right_box=[1280-640, 720-480],
            bottom_left_box=[0, 720-480]).items():
        cv2.namedWindow(window_name)
        cv2.moveWindow(window_name, *v)
        for expression_id in range(5):
            path = _capture_session(expression_id, stop_after, f'{k} {comments}')
            print('Capture session path', path)

# Cell
@call_parse
def viseme_dataset_from_capture_sessions(
        input_path:Param('Path to read capture session data from', str)='data/capture_session',
        glob_pattern:Param('Pattern of folders to include', str)='viseme*'):
    "Create a viseme dataset from capture session data"
    path = _viseme_dataset_from_capture_sessions(input_path, glob_pattern)
    print('Viseme dataset path', path)

# Cell
@call_parse
def processed_dataset_from_viseme_dataset(
        input_path:Param('Path to read viseme data from', str),
        landmark_ids:Param('Comma separated list of landmarks IDs (int) to include', str),
        relative_landmark_id:Param('ID of landmark that other landmarks should be made relative to', int)=None,
        y_name:Param('Name of the target variable', str)='expression_id',
        change_y_from:Param('Target value to change from', int)=None,
        change_y_to:Param('Target value to change to', int)=None):
    "Create a processed dataset (ready for ML) from a raw viseme dataset"
    # TODO: make landmark_ids parse more robust - or use config file to drive processing
    landmark_ids = [int(i) for i in landmark_ids.split(',')]
    path = _processed_dataset_from_viseme_dataset(
            input_path, landmark_ids, relative_landmark_id, y_name, change_y_from, change_y_to)
    print('Viseme dataset path', path)