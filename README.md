Automatic Image Annotation
--------------------------
--------------------------


Overview
--------
This project is a collaboration between Connor Grimberg and Joseph Lee Our goal is to use a convolutional neural network on a web application to identify types of disasters in images. Our current goal is to have our neural network perform multi-label classification, identifying not only the type of disaster found in the image but also relevant details important for search and rescue teams, such as damage done to buildings and / or vegetation.(add more to this as we progress)


Requirements
------------

Python 3.7
pytorch 1.3.0


Installation
------------

Download all the files and change the path variable in "webapp.py" to the location of the "export.pkl" file.


Running
-------

In the terminal cd to the location of the webapp. Then do "streamlit run webapp.py"
