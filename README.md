# NEUROEVOLVER
Software focused in neuroevolution using the algorithm NEAT.

![alt text](https://github.com/VgTajdd/neuroevolver/blob/master/neuroevolver.png)
![alt text](https://github.com/VgTajdd/neuroevolver/blob/master/neuroevolver_reducido_train.gif)

## Initial considerations

This project was developed in Windows, so the current README have valid instructions for this OS. 

This project was developed used Python 3.7, so it's recommended to use this version. If you prefer to use another version, it's possible that some changes need to be done.

## Prepare everything

To get the repository you could use ```git clone https://github.com/VgTajdd/neuroevolver.git``` or simply download the zip file.

Install Python. Once Python is ready to be used, install virtualenv:

```bash
pip install virtualenv
```
Then, it's necessary to have SWIG, you can download it from [here](http://www.swig.org/download.html).

At this point, you need to make the **SWIG_PATH** variable (in the script **install_requirements_in_venv.bat**) and your SWIG path (where you extracted/installed SWIG) equal.

Finally, update the file **python_home** with your PYTHON HOME directory.

## Usage

### Create virtual environment

```bash
create_virtualenv.bat
```

### Install all dependencies

```bash
install_requirements_in_venv.bat
```

### Run the program

```bash
run.bat
``` 

At this point, if you prefer, you can use Visual Studio.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
