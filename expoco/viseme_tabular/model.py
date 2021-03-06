# AUTOGENERATED! DO NOT EDIT! File to edit: 10d_viseme_tabular_model.ipynb (unless otherwise specified).

__all__ = ['save_state_dict', 'load_state_dict', 'NpBatchNorm1d', 'NpLinear', 'NpReLU', 'NpModel', 'get_class_count',
           'load_tabular_model', 'create_confusion_matrix', 'plot_confusion_matrix', 'get_idxs_of_interest']

# Cell
from ..core import *
from pathlib import Path
import numpy as np
import json

# Cell
def save_state_dict(path, state_dict, **training_info):
    "Saves `state_dict` and `training_info` to a new model directory"
    path, model_id = Path(path), now()
    output_path = path/f'model_{model_id}'
    output_path.mkdir()
    file_name = output_path/'state_dict.npz'
    metadata = dict(path=path_to_str(path), output_path=path_to_str(output_path),
                    file_name=path_to_str(file_name), training_info=training_info)
    with open(output_path/'metadata.json', 'w') as f: json.dump(metadata, f, indent=2)
    np.savez(file_name, **{k:state_dict[k].detach().cpu().numpy() for k in state_dict})
    with np.load(file_name) as _: pass # check that we didn't need to pickle
    return output_path

# Cell
def load_state_dict(path):
    "Load `state_dict.npz` from `path` (a model directory)"
    return np.load(Path(path)/'state_dict.npz')

# Cell
class NpBatchNorm1d:
    "Applies Batch Normalization"
    # https://github.com/pytorch/pytorch/blob/420b37f3c67950ed93cd8aa7a12e673fcfc5567b/aten/src/ATen/native/Normalization.cpp#L61-L126
    def __init__(self, weight, bias, running_mean, running_var, num_batches_tracked=None):
        self.weight, self.bias = weight, bias
        self.running_mean, self.running_std = running_mean, np.sqrt(running_var + 1e-5)
    def __call__(self, x):
        x = x - self.running_mean
        x = x / self.running_std
        x = x * self.weight
        x = x + self.bias
        return x

# Cell
class NpLinear:
    "Applies a linear transformation"
    def __init__(self, weight, bias=None):
        self.weight, self.bias = weight.T, bias
    def __call__(self, x):
        x = x @ self.weight
        if self.bias is not None:
            x = x + self.bias
        return x

# Cell
class NpReLU:
    "Applies element wise max of x and zero"
    def __call__(self, x):
        return np.maximum(x, 0)

# Cell
class NpModel:
    "A sequential module container"
    def __init__(self, *modules):
        self.modules = modules
    def __call__(self, x):
        for module in self.modules:
            x = module(x)
        return x

# Cell
def get_class_count(model):
    return model.modules[-1].weight.shape[1]

# Cell
def load_tabular_model(path):
    "Load `state_dict.npz` from `path` (a model directory) and create a tabular model"
    state_dict = load_state_dict(path)
    # TODO: this only works for the model config we used ... TODO: make it a bit more generic
    return NpModel(NpBatchNorm1d(**get_dict_subset(state_dict, 'bn_cont')),
                   NpLinear(**get_dict_subset(state_dict, 'layers.0.0')),
                   NpReLU(),
                   NpBatchNorm1d(**get_dict_subset(state_dict, 'layers.0.2')),
                   NpLinear(**get_dict_subset(state_dict, 'layers.1.0')),
                   NpReLU(),
                   NpBatchNorm1d(**get_dict_subset(state_dict, 'layers.1.2')),
                   NpLinear(**get_dict_subset(state_dict, 'layers.2.0')))

# Cell
def create_confusion_matrix(model, df, cont_names, y_name):
    "Confusion matrix as a numpy array"
    class_count = get_class_count(model)
    confusion_matrix = np.zeros([class_count,class_count], dtype=int)
    output = model(df[cont_names].to_numpy())
    preds = np.argmax(output, axis=1)
    _class_to_id = dict(AH=0, EE=1, NO_EXPRESSION=2, OO=3) # TODO: train tabular model, save class map in metadata
    targets = _data[y_name].apply(lambda v: _class_to_id[v]).to_list()
#     targets = df[y_name].to_numpy(dtype=int)
    for p,t in zip(preds, targets):
        confusion_matrix[t][p]+=1
    return confusion_matrix

# Cell
def plot_confusion_matrix(model, df, cont_names, y_name):
    "Plot a confusion matrix using matplotlib"
    confusion_matrix = create_confusion_matrix(model, df, cont_names, y_name)
    class_count = get_class_count(model) # class_count might not be the same as len(class_ids)
    class_ids = [0,1,2,3] # TODO: train tabular model, save class map in metadata
    class_labels = ['AH', 'EE', 'NO_EXPRESSION', 'OO']
    fig, ax = plt.subplots(figsize=(9,9))
    ax.matshow(confusion_matrix, cmap=plt.cm.Blues, alpha=0.8)
    # ax.xaxis.set_ticks_position('bottom') # must be after matshow
    ax.yaxis.set_label_position('right')
    for i in range(confusion_matrix.shape[0]):
        for j in range(confusion_matrix.shape[1]):
            ax.text(x=j, y=i,s=confusion_matrix[i, j], va='center', ha='center', size='xx-large')
    plt.title('Confusion Matrix', fontsize=14)
    plt.xlabel('Predicted', fontsize=12)
    plt.ylabel('Actual', fontsize=12)
    tick_marks = np.arange(class_count)
    plt.xticks(tick_marks, class_labels[:class_count], rotation=90)
    plt.yticks(tick_marks, class_labels[:class_count], rotation=0)
    plt.show()

# Cell
def get_idxs_of_interest(model, df, cont_names, y_name, target_of_interest, pred_of_interest):
    "Indeces in `df` where `df[y_name]` had `target_of_interest` but the model predicted `pred_of_interest`"
    class_labels = ['AH', 'EE', 'NO_EXPRESSION', 'OO'] # TODO: train tabular model, save class map in metadata
    output = model(df[cont_names].to_numpy())
    preds = np.argmax(output, axis=1)
    _class_to_id = dict(AH=0, EE=1, NO_EXPRESSION=2, OO=3) # TODO: train tabular model, save class map in metadata
    targets = _data[y_name].apply(lambda v: _class_to_id[v]).to_numpy()
#     targets = df[y_name].to_numpy()
    idxs = []
    print('target_of_interest', class_labels[target_of_interest],
          'pred_of_interest', class_labels[pred_of_interest])
    print('overall accuracy', (targets==preds).sum() / len(targets))
    _filter = targets==target_of_interest
    print('accuracy for target_of_interest',(targets[_filter]==preds[_filter]).sum() / _filter.sum())
    for i, (p,t) in enumerate(zip(preds,targets)):
        if t==target_of_interest and p==pred_of_interest:
            idxs.append(i)
    return idxs