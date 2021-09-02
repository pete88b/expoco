# ExPoCo: Expression Pointer Control
> This project attempts to find ways of controling your pointer (cursor) with as little mouse use as possible.


# Coding conventions

`point`: 2 tuple or list. e.g. `(x, y)` or `[x,y]`

`size`: 2 tuple or list. e.g. `screen_size = [screen_width, screen_height]`

## Install

`pip install expoco`

# Developers

If you're working on a windows machine
```
git config --global core.autocrlf input
```

To setup a conda environment for local development
```
conda create -n expoco python==3.7 -y
conda activate expoco
pip install nbdev jupyterlab opencv-python
cd github *** nav to where you want this project to live on your filesystem
git clone https://github.com/pete88b/expoco.git
cd expoco
nbdev_install_git_hooks
jupyter-lab
```

2021-09-01: I ran the above, then `pip freeze > requirements.txt` to create requirements.txt
