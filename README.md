Disaster Autotations
--------------------------
--------------------------

* Note: still work in progress. (I have yet to test if the instructions below will actually work.) Hopefully though, the rest of this README should give you a solid foundation of this project's structure. 

Video Presentation
----------------
https://www.youtube.com/watch?v=l40CRMz0cWo

General Overview
----------------
This repository contains the code and other files written during our senior research project. Our goal is to use a convolutional neural network on a web application to identify types of disasters in images. We have two convolutional neural networks (CNNs), one for multi-class classification, identifying disaster type, and another for multi-label classification, identifying not only the type of disaster found in the image but also relevant details important for search and rescue teams, such as damage done to buildings and/or vegetation.

We ended up with using two CNNs instead of just a multilabel because our single-label was accurate/very skilled at (~95.6% accuracy) identifying the type of disaster, while our multilabel CNN (~59.8% accuracy) was not as well off on its own. We thought the two CNNs could both both display their results so users could compare the two results and give feedback whenever neccessary. 


Code Overview
-------------
The "code" folder includes Jupyter Notebooks that we used to train the artificial intelligence model (using Convolutional Neural Network frameworks), in addition to all the files used for the web application development. 


Neural network training files:
gdrive_fastai_CNN.ipynb was the "final draft" for the single-label neural network model. 
MultiLabel NN Training.ipynb was the "final draft" for the multi-label neural network model. 

All other Jupyter notebooks were "rough drafts." We decided to move on with new Jupyter notebooks, some of which ended up as "final drafts."


Web application files:
"autotations.py" was the Python file responsible for running the web application. 
(Anything else with the commit message "Director Code" means that it was a file used for the web app development process of our project.) 

(Insert web app development file structure here.)  

Requirements
------------

We used Python, PyTorch (ended up not working) framework, fast.ai (ended up working) framework, Streamlit API


Installation
------------

Clone this project or download all the files under the "code" folder and change the path variable in "autotations.py" to the location of the "export.pkl" file.


How to Run
-------

(Ignore below for now; work in progress)
In the terminal change directory to "code" and then to "autotations.py". Then do "streamlit run autotations.py"

Website
-------
https://disaster_autotations.sites.tjhsst.edu

(used to be open-access, but now restricted (this was hosted on school servers). I have plans to make the project website hosted at a different online location.) 
