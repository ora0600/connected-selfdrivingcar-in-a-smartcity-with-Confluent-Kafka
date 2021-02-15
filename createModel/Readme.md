# Create your own model

Of course you can produce your own model.
Before creating your own model, you have to have the right software. I use Anaconda and Python on my Mac.
* Install Anaconda on Mac see [Installation Guide](https://docs.anaconda.com/anaconda/install/mac-os/)
* Have Python 3 running
* install important python modules

After installation of Anacondo and Python we need add additionaly Phyton moduls
```bash
# I have more than one version of python running, we need version 3.8 at the end
brew install python@3.7
brew install python@3.8
brew install python@3.9
brew unlink python@3.9
brew unlink python@3.8
brew unlink python@3.7
brew link python@3.8
# Conda
conda install nb_conda
# create tensorflow namespace and install packages in python 3.8
conda create -n tf tensorflow
conda activate tf
conda install pandas matplotlib jupyter notebook scipy scikit-learn nb_conda nltk  spyder tensorflow keras
conda install opencv
conda install -c anaconda flask
conda install -c conda-forge python-socketio
conda install -c conda-forge eventlet
conda install -c conda-forge Pillow
conda install -c conda-forge python-engineio=2.2.0
```

## Creating the model
The model will be created in Jupyter Notebook.
Open Anaconda, show the environment tf and open in environment tf Jupyter Notebook.
Open the noetbook `CreateModel4selfdrivingcar.ipynb` which belongs to this github project.
At the beginning of the notebook you will see one git clone command.
```bash
!git clone https://github.com/ora0600/track
```
These are tracking information, which I did upload to a separate github repo. These tracking information will be used to train the model.
Tracking information can created by yourself. Open the UDACITY App, enter training mode and record the training by clicking on the button. Please, use 800x600 resolution. A csv file and 3 images per position will be tracked. For a good a training you need to drive at least 3 rounds.
Maybe you be able to train a better model than me.

If you need more input what the specific steps in the notebook you can check these information:
* [self-driving-car demo at udemy.com](https://www.udemy.com/course/applied-deep-learningtm-the-complete-self-driving-car-course/)
