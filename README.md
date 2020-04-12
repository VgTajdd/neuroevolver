# NEUROEVOLVER
Software focused in neuroevolution using the algorithm NEAT.

![alt text](https://github.com/VgTajdd/neuroevolver/blob/master/neuroevolver.png)
![alt text](https://github.com/VgTajdd/neuroevolver/blob/master/neuroevolver_reducido_train.gif)

## Pygame installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pygame.

```bash
pip install pygame
```

## Box2d-py
Enable a virutal env if you prefer to work there.
Include this environment variable in your PATH (local or global), for example:
```
set local
set SWIG_PATH=C:path/to/swigwin-3.0.12
set PATH=%SWIG_PATH%;%PATH%;
cmd /k
endlocal
```

There are 2 ways to install Box2d-py

1. Using [pip](https://pip.pypa.io/en/stable/):
```bash
pip install box2d-py
```
2. Using ```setuptools```, go to directory of ```setup.py``` and use this commands (build and install):
```bash
python setup.py build
python setup.py install
```
We won't install pgu, because it's only avialable for ```python 2.x```, but if you want to install this, follow the next instructions.

- Download de source code, (pip is not avialable for this package).
- Install by using ```setuptools```, go to directory of ```setup.py``` and use this commands (build and install):
```bash
python setup.py build
python setup.py install
```
## Special considerations

- fix the paths (in the bat files) for your global python installation
- install virtualenv in your global python installation: pip install virtualenv

## Usage

Once you have all the dependecies installed follow this steps:

- create_virtualenv.bat
- install_requirements_in_venv.bat
- run.bat

At this point, if you prefer, you can use visual studio to make your changes.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
