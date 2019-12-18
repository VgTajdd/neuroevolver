# NEUROEVOLVER
NEUROEVOLVER is an application focused in neuroevolution using the algorithm NEAT.

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

1-instalar box2d-py usando pip:
    pip install box2d-py

2-instalar usando setuptools desde código(compilar e instalar):
	(ir al directorio donde esta el setup.py)
	python setup.py install
	python setup.py build

Instalar pgu(no se usará por ahora ya que solo esta para python 2.x)

Descargar el código ya que no hay instalación por pip e instalar con setuptools:

instalar usando setuptools desde código(compilar e instalar):
	(ir al directorio donde esta el setup.py)
	python setup.py install
	python setup.py build


## Usage
```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
