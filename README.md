Disaster Autotations
--------------------------
--------------------------

* Note: still work in progress. (I have yet to test if the instructions below will actually work, since the "code" folder has code from all over the place. Hopefully though, observing the specified files mentioned below should give you an idea.) 

The "code" folder includes Jupyter Notebooks that we used to train the artificial intelligence model (using Convolutional Neural Network frameworks), in addition to all the files used for the web application development. 


Neural network training files:
gdrive_fastai_CNN.ipynb was the "final draft" for the single-label neural network model. 
MultiLabel NN Training.ipynb was the "final draft" for the multi-label neural network model. 

All other Jupyter notebooks were "rough drafts." We decided to move on with new Jupyter notebooks, some of which ended up as "final drafts."


Web application files:
"autotations.py" was the Python file responsible for running the web application. 
(Anything else with the commit message "Director Code" means that it was a file used for the web app development process of our project.) 

(Insert web app development file structure here). 

Overview
--------
This repository contains the code and other files written during our senior research project. Our goal is to use a convolutional neural network on a web application to identify types of disasters in images. We have two convolutional neural networks, one for multi-class classification, identifying disaster type, and another for multi-label classification, identifying not only the type of disaster found in the image but also relevant details important for search and rescue teams, such as damage done to buildings and/or vegetation.


Requirements
------------

We used Python, PyTorch (ended up not working) framework, fast.ai (ended up working) framework, Streamlit API


Installation
------------

Download all the files and change the path variable in "autotations.py" to the location of the "export.pkl" file.


Running
-------

In the terminal change directory to "code" and then to "autotations.py". Then do "streamlit run webapp.py"

Website
-------
https://disaster_autotations.sites.tjhsst.edu

(used to be open-access, but now restricted. I have plans to make the project website hosted at a different online location.) 
