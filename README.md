# neuroevolver

Neuroevolution software

########################################

Instalar box2d-py

Descargar swig para windows (swigwin-3.0.12.zip, o alguna version que se pueda usar para windows). Descomprimir y ubicar en una ubicación estrategica para luego usar el swig.exe que esta adentro (por ejemplo C:\swigwin-3.0.12)

Pasos:

- pygame instalado

- activar el entorno virtual si es el caso, incluyendo en el PATH (local) la variable de entorno, por ejemplo:

set local
set SWIG_PATH=C:path/to/swigwin-3.0.12
set PATH=%SWIG_PATH%;%PATH%;
cmd /k
endlocal

de no ser el caso de un entorno virtual, igual agregar la variable SWIG_PATH al PATH (sea localmente o globalmente).

- acá llegamos a dos forma de instalacion:

1-instalar box2d-py usando pip:
    pip install box2d-py

2-instalar usando setuptools desde código(compilar e instalar):
	(ir al directorio donde esta el setup.py)
	python setup.py install
	python setup.py build

########################################

Instalar pgu(no se usará por ahora ya que solo esta para python 2.x)

Descargar el código ya que no hay instalación por pip e instalar con setuptools:

instalar usando setuptools desde código(compilar e instalar):
	(ir al directorio donde esta el setup.py)
	python setup.py install
	python setup.py build
