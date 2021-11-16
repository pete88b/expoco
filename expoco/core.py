# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['in_colab', 'in_jupyter', 'in_notebook', 'now', 'path_to_str', 'get_dict_subset', 'FaceLandmarks',
           'VisemeConfig', 'landmark_ids_to_col_names', 'ImageDisplayHelper', 'LogFile']

# Cell
from dataclasses import dataclass
from pathlib import Path
import cv2, datetime, json, time

# Cell
def in_colab():
    "Check if the code is running in Google Colaboratory"
    try:
        return 'google.colab' in str(get_ipython())
    except:
        return False

def in_jupyter():
    "Check if the code is running in a jupyter notebook"
    try:
        return 'ZMQInteractiveShell' in str(get_ipython())
    except:
        return False

def in_notebook():
    "Check if the code is running in a jupyter notebook"
    return in_colab() or in_jupyter()

# Cell
def now():
    "Return a timestamp string that can be used in file or directory names"
    return datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')

# Cell
def path_to_str(path):
    "Format a path so that path strings can be used on different platforms"
    return str(path).replace('\\', '/')

# Cell
def get_dict_subset(d, name_prefix, remove_prefix=True, remove_additional_characters=1):
    "Return a subset of entries from a dictionary like object"
    if name_prefix is None or name_prefix == '': return d
    def _rm_prefix(k):
        if not remove_prefix: return k
        return k[len(name_prefix)+remove_additional_characters:]
    return {_rm_prefix(k): d[k] for k in d if k.startswith(name_prefix)}

# Cell
@dataclass(frozen=True) # frozen doesn't really help (o: but we don't want to change values of this data class
class FaceLandmarks:
    "Constants to help working with facemesh landmarks"
    count=468
    top_lip_indent=0
    tip_of_nose=1
    pointer = [1, 5, 2, 218, 438] # tip_of_nose,up,down,left,right
    mouth = [0, 11, 12, 13, 14, 15, 16, 17, 18, 37, 38, 39, 40, 41, 42, 43, 57, 61, 62, 72, 73, 74, 76, 77, 78, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 95, 96, 106, 146, 164, 165, 167, 178, 179, 180, 181, 182, 183, 184, 185, 186, 191, 204, 267, 268, 269, 270, 271, 272, 273, 287, 291, 292, 302, 303, 304, 306, 307, 308, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 324, 325, 335, 375, 391, 393, 402, 403, 404, 405, 406, 407, 408, 409, 410, 415, 424]

# Cell
class VisemeConfig: # TODO: do we want to use generic metadata for all datasets?
    def __init__(self, path='data'):
        with open(Path(path)/'viseme-config.json') as f:
            self.config = json.load(f)
    def get_class_label(self, class_id):
        return self.config['expressions'][str(class_id)]
    def get_class_ids_and_labels(self):
        items = self.config['expressions'].items()
        return [int(i) for i, j in items], [j for i, j in items]
        # we could use the bellow, if we didn't have to convert class IDs to int
        # return list(zip(*self.config['expressions'].items()))

# Cell
def landmark_ids_to_col_names(landmark_ids, landmark_ids_to_exclude=None, coords=['x','y']):
    "Convert landmark IDs and coords into column names"
    landmark_ids, coords, col_names = sorted(landmark_ids), sorted(coords), []
    if not isinstance(landmark_ids_to_exclude, list):
        landmark_ids_to_exclude = [landmark_ids_to_exclude]
    for i in landmark_ids:
        if i in landmark_ids_to_exclude:
            continue
        for coord in coords:
            col_names.append(f'{i}{coord}')
    return col_names

# Cell
class ImageDisplayHelper:
    "Display images in-notebook or standalone depending on runtime"
    def __init__(self, image, name='image'):
        "Create a new helper and show the image"
        self.name, self.in_notebook = name, in_notebook()
        self.show(image)
    def show(self, image):
        "Show an image"
        self.show_ipywidget(image) if self.in_notebook else self.show_cv2(image)
    def show_cv2(self, image):
        "Show an image using cv2"
        cv2.imshow(self.name, image)
        cv2.waitKey(1)
    def show_ipywidget(self, image):
        "Show an image using a jupyter widget"
        if getattr(self, 'image_widget', None) is None:
            import ipywidgets as widgets
            self.image_widget = widgets.Image(value=cv2.imencode('.png', image)[1].tobytes())
            display(self.image_widget)
        else:
            self.image_widget.value = cv2.imencode('.png', image)[1].tobytes()
    def close(self):
        "Close the image display"
        if getattr(self, 'image_widget', None) is not None:
            self.image_widget.close()
        cv2.destroyAllWindows()

# Cell
class LogFile: # TODO: if we capture everything in metadata, we don't need the logs
    def __init__(self, path):
        self.path = Path(path)
        print('LogFile:', self.path.resolve())
    def __call__(self, *args):
        with open(self.path, 'a') as f:
            f.write(' '.join([str(arg) for arg in args]) + '\n')
        return self