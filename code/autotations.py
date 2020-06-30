import streamlit as st
import pandas as pd
import numpy as np 

from base64 import b64decode
from PIL import Image
import urllib.request
import requests
from io import BytesIO
import torch
from fastai.vision import *
import csv

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pickle
import os

# STREAMLIT_SERVER_MAXUPLOADSIZE = 2

# @st.cache
def gdriveAuth():
    driv = "instantiating"
    with open("auth.pkl", 'rb') as input: 
        driv = pickle.load(input)
    return driv

drive = gdriveAuth()

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """

st.markdown(hide_menu_style, unsafe_allow_html = True)

tab_title = '''
    <head>
        <title> Disaster Autotations </title>
    </head>
    '''

st.markdown(tab_title, unsafe_allow_html = True)

# html = """
#   <style>
#     .reportview-container {
#       flex-direction: row-reverse;
#     }

#     header > .toolbar {
#       flex-direction: row-reverse;
#       left: 1rem;
#       right: auto;
#     }

#     .sidebar .sidebar-collapse-control,
#     .sidebar.--collapsed .sidebar-collapse-control {
#       left: auto;
#       right: 0.5rem;
#     }

#     .sidebar .sidebar-content {
#       transition: margin-right .3s, box-shadow .3s;
#     }

#     .sidebar.--collapsed .sidebar-content {
#       margin-left: auto;
#       margin-right: -21rem;
#     }

#     @media (max-width: 991.98px) {
#       .sidebar .sidebar-content {
#         margin-left: auto;
#       }
#     }
#   </style>
# """
# st.markdown(html, unsafe_allow_html=True)
 
# st.sidebar.text("I'm here now.")


# @st.cache
# def load_data(nrows):    # nrows is number of rows it will read.
#     data = pd.read_csv("annotations_earthquake.csv", nrows=nrows)
#     return data

single_classes = ['earthquake', 'fire', 'flooding', 'hurricane', 'normal']
multi_classes = [
  "bridge",
  "earthquake",
  "fire",
  "flooding",
  "high_vegetation",
  "hurricane",
  "low_vegetation",
  "normal",
  "river",
  "road",
  "rough_terrain",
  "struct_damage"
]

mimetypes = { # this rn makes all spreadsheet downlads csv files instead
  "application/vnd.google-apps.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "csv": "text/csv",
  "pickle_file": "application/octet-stream"
}

# st.sidebar.title("Extra Information")
st.title("Disaster Autotations")

st.write("<style> .reportview-container .main .block-container {padding: 0rem} </style>", 
        unsafe_allow_html = True)



def user_image(link):
    try:
        data = requests.get(link)
        #data = (requests.urlopen(requests.Request(link))).read()
        img = BytesIO(data.content)
        return img
    except:
        try:
            header, encoded = link.split(",", 1)
            img = BytesIO(b64decode(encoded))
            return img
        except:
            return 'None'




# @st.cache
def predict_img(img):
    img = open_image(img)  # open_image is a fast.ai built-in method
    defaults.device = torch.device('cpu')
    path = Path("") / 'models'
    #path = Path('public/data')
    #data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.5,
    #    ds_tfms=get_transforms(), size=224, num_workers=4).normalize(imagenet_stats)
    #/web/projects/streamlit2/public")#/export.pkl")
    #learn = cnn_learner(data, models.resnet34, metrics=error_rate)
    #learn.load_state_dict(torch.load(path))
    s_learn = load_learner(path, 'single.pkl') 
    m_learn = load_learner(path, 'multi.pkl')
    return (s_learn.predict(img), s_learn.data.classes), (m_learn.predict(img), m_learn.data.classes)

fragments = []    
# def form_to_english(list_of_anns):
#     fragments = list_of_anns[:]
#     for i in range(len(list_of_anns)):
        
#     for ann in list_of_anns:
#         to_ret += "<li> "
    
# @st.cache
def highlight_max(s):    
    is_max = s == s.max()
    return ['color: red' if v else '' for v in is_max]

def img_to_CNN(img, key):
    if img == 'None':
        st.write("Invalid Image URL. Please try a different image.")
        
    else:                                                     # checks if there is a valid image inputted
        gdriveAuth()                                            # gives code access to my gdrive
        
        # try:
        st.image(PIL.Image.open(img), use_column_width=True)    # displays image
        
        ((pred_class, pred_idx, s_probs), s_classes), \
        ((pred_classes, pred_idxs, m_probs), m_classes) = predict_img(img)                          # runs image through nn and returns various outputs
        #st.write(p_c)
        #st.write(p_i)
        #st.write(o)

        certainty_df = (pd.DataFrame(np.matrix(s_probs), columns=[x for x in s_classes]) * 100).round(1)   #
        certainty_df = certainty_df.astype(str) + '%'
        certainty_df.rename(index={0:"Probability"}, inplace=True)                  # Displaying output in table form
        st.dataframe(certainty_df.style.apply(highlight_max, axis=1))             # 
        st.write(pred_classes)
    
        # s = str(o[single_classes.index(str(p_c))])
        # s = s[8:len(s)-1]
        # s = float(s)*100
        # st.write(str(s) + "%")
        
        st.write("Am I wrong? (Under implementation--don't click on this just yet.)")                        # writes was I wrong
        if st.checkbox("Yes.", key = key):              # creates checkbox and sees if it is checked
            # models option is only here for testing
            dtype = st.radio("Which disaster is in the picture?", ["earthquake", "hurricane", "fire", "flooding", "normal"], key = key) # creates the list of buttons
            if st.button("Confirm", key = key): # creates confirm button and checks if pressed
                filename = dtype + ".csv" # + "_urls.csv"       # filenames in gdrive are "flooding.csv" etc. so this makes filename variable replicate that
                fileList2 = drive.ListFile({'q': ("'1KULt0NcduggNwn-60-8jR9Azx8BpAE6Y' in parents and trashed=false")}).GetList() # opens that folder
                for file2 in fileList2: # searches for the csv file to edit
                    # requires old version of file to exist already
                    if file2['title'] == filename:
                        file_obj = drive.CreateFile({'id': file2['id']})      # once found,
                        file_obj.GetContentFile(filename, mimetypes["csv"])   # download the csv file
                        with open(filename, "a", newline='\n') as fd:  #
                            csv_writer = csv.writer(fd)
                            csv_writer.writerow([url])#, ',', ',',',',',',',',',',',',',',','])
                            
                            
                            
                            
                            # fieldnames = ["url", "none"]
                            # writer = csv.DictWriter(fd, fieldnames=fieldnames, lineterminator='\n')      # add new url to end of csv
                            # # csv should probably have stuff in it already
                            # #none = "",,,,,,,,,
                            # writer.writerow({"url": url, "none":'\n'})       # 
                            
                            
                            
                            
                            
                        file_obj = drive.CreateFile({'mimeType': mimetypes["csv"], 'id': file2['id']})  #
                        file_obj.SetContentFile(filename)                                               # replace old file with edited file
                        file_obj.Upload()                                                               # 
                os.remove(filename)             # remove the edited file that exists on director
                fileList = drive.ListFile({'q': "'1T5WKP7xSRb5HAsbu2aLfQFmaoUz4rUt4' in parents and trashed=false"}).GetList() #
                for file in fileList:                                                                                          # Downloads the latest best models
                    file_obj = drive.CreateFile({'id': file['id']})                                                            # Note: This section might move 
                    file_obj.GetContentFile('export.pkl', mimetypes["pickle_file"])                                            # somewhere else in the code
                    
                    
                st.write("Pushing this button more than once will append its url to the dataset more than once.") # Writing a warnign because
                st.write("Unless you want this to happen, please don't push again.")                              # it is possible to have the same url multiple times
                
        # except:
        #     st.write("Invalid Image URL. Please try a different image.")

if st.checkbox('Insert link option'):
    url = st.text_input("Insert link to image")
    
    if url:
        img = user_image(url)
        img_to_CNN(img, key = 'link')

if st.checkbox('Upload image option'):
    uploaded_img = st.file_uploader('Upload image here', type = ['jpg', 'png'])
    # resized_img = PIL.Image.open(uploaded_img).resize((500, 500))
    
    if uploaded_img:
        img_to_CNN(uploaded_img, key = 'upload')
    
    else:
        st.info("Please upload a file of type: " + ", ".join(['jpg', 'png']))
    

# if url or uploaded_img:
#     img = user_image(url) if url else uploaded_img






d_text_0 = '''
### Greetings and Setup
Welcome to Disaster Autotations (Autotations = Automatic Annotations). Choose one of the above options to input an aerial 
photo ending in representing a disaster (i.e. fire, earthquake, flood, hurricane, or normal (i.e. no disaster)) to the bar above and 
see Artificial Intelligence figure out what type of disaster and other relevant details inside the photo you inputted.
Here is an example of a link you can input: https://i.ytimg.com/vi/uBT8j2L6m_k/hqdefault.jpg

'''

d_text_1 =  '''

### Instructions  
1. Go to https://images.google.com  
2. Search up an aerial image of a disaster (e.g. "Hurricane Katrina aerial photo")   
3. Choose an image   
4. Right click on that image, then left click on "Copy image address"  
5. Paste that address to the "Insert link to image" bar 

**Make sure NOT to input ground-level nor satellite-level images** (explanation in "↓ More info. ↓").

### Feedback
Should this web application classify an image incorrectly, correct it
through the "Am I wrong?" button. Thank you. '''

d_text_2 = '''

### Background
Within the last 20 years, natural disasters have killed 1.3 million people and impacted 4.4 billion people, and 56% have been caused by earthquakes and tsunamis. Costs to recover from these disasters have risen 151%. While these stats are alarming, they may potentially be on the rise in the future, as the rate of natural disasters continues to grow. As a result of this eminent danger, disaster response has grown as a field. The federal government has become involved with the establishment of the Federal Emergency Management Agency (FEMA), whose primary job is to give funding to disaster team organizations. One such organization is the Civil Air Patrol (CAP).  CAP is a non-profit, public service organization focused around carrying out emergency services and disaster relief mission nationwide while serving as a supplement to the United States Air Force.

CAP trains American soldiers to fly aircraft to take representative aerial photos of areas surrounding natural disasters for the purposes of disaster assessment and potentially to figure out which locations have priority status in resource allotment (e.g. how many people are sent, how much food is sent, and how much time is spent there.) 

Here is a link for more context:
https://bit.ly/2Sg0957
'''

d_text_3 = '''

### Motivation 
Lives are on the line here; every second counts in a disaster response. My partner and I believed that Artificial Intelligence had potential to speed up the disaster response. More specifically, we envisioned an autonomous system (i.e. drones or any autonomous aircraft) can then leverage that Artificial Intelligence to detect priority locations for disaster teams such as the Civil Air Patrol to go, based on the interest of maximizing the number of people saved. Currently in disaster response, humans analyze the state of a disaster in aircraft and in the ground for further inspection. However, this can cause harm, especially for those on the ground. Autonomy can therefore bring in further safety for disaster response as well. 



### Our Solution
Therefore, we decided our solution was a web application designed to assist the Civil Air Patrol (CAP) and other disaster
responders with sorting out aerial disaster imagery to figure out the most vital locations
to go to first. Our source of motivation comes from https://github.com/mit-ll/PSIAP-CAP-Annotation,
a project that worked on semantic annotations from Civil Air Patrol imagery. We wanted to autonomize
that process to help save lives in future disasters.  

### Progress and For the Future
Currently, this web application is capable of classifying whether a given image has a certain 
disaster (i.e. earthquake, fire, flooding, hurricane, normal) in it. We are working on making it classify more relevant details
important for disaster responders, such as structural damage and vegetation. The ultimate
goal we work towards is the capability for this web application to take in a folder of images from the CAP,
autonomously annotate them, rank them on a severity scale, and output the most vital
locations for rescue teams to be sent off to (perhaps similar to the map seen below). 
'''


st.write(d_text_0)

# first_image_url = 'https://i.ytimg.com/vi/uBT8j2L6m_k/hqdefault.jpg'
# first_image = PIL.Image.open(urllib.request.urlopen(first_image_url))
# st.image(first_image, use_column_width = True)

#Brings sidebar text more to the top (to make "More info." more visible)
st.write("<style> .sidebar .sidebar-content {padding: 0rem 1rem} </style>", unsafe_allow_html = True)

if st.checkbox("A way to find links + more info."):
    st.sidebar.markdown(d_text_1)
    
    st.sidebar.title('↓ More info. ↓')
    st.sidebar.markdown(d_text_2)
    
    h_mich_img = PIL.Image.open('./images/Hurricane Micheal.jpg')
    cap_img = PIL.Image.open('./images/CAP.jpg')
    
    st.sidebar.image(h_mich_img, use_column_width = True, caption = 'Hurricane Michael (as a category four storm) aftermath in the Florida Panhandle.')
    st.sidebar.image(cap_img, use_column_width = True, caption = 'CAP Pilot taking aerial photos of Hurricane Sandy.')
    
    st.sidebar.markdown(d_text_3)
    
    map_image = PIL.Image.open('./images/wildfire-activity-map-01.jpg')
    st.sidebar.image(map_image, use_column_width = True, caption = 'Wildfire Activity Map')
    
    
# if st.checkbox("Sources"):
#     # sources = PIL.Image.open('./images/sources.jpg')
#     # st.image(sources, use_column_width = True)
#     source_html = "<a href = https://user.tjhsst.edu/2020jlee/auto_anns_sources> Sources </a>"
    
#     st.write(source_html, unsafe_allow_html = True)

source_html = "<a href = https://user.tjhsst.edu/2020jlee/auto_anns_sources target = _blank> Sources </a>"
st.write(source_html, unsafe_allow_html = True)
    
# if st.checkbox("More info."):
#     if bool_first_checkbox:
#         first_sidebar.title('Scroll down!')
        
#     st.sidebar.markdown(d_text_2)
    
#     h_mich_img = PIL.Image.open('Hurricane Micheal.jpg')
#     cap_img = PIL.Image.open('CAP.jpg')
    
#     st.sidebar.image(h_mich_img, use_column_width = True, caption = 'Hurricane Michael (as a category four storm) aftermath in the Florida Panhandle.')
#     st.sidebar.image(cap_img, use_column_width = True, caption = 'CAP Pilot taking aerial photos of Hurricane Sandy.')
    
#     st.sidebar.markdown(d_text_3)
    
#     map_image = PIL.Image.open('wildfire-activity-map-01.jpg')
#     st.sidebar.image(map_image, use_column_width = True, caption = 'Wildfire Activity Map')
    
#     st.sidebar.markdown('### Sources')
    
#     sources = PIL.Image.open('sources.jpg')
#     st.sidebar.image(sources, use_column_width = True)




# st.write(d_text_1)

# This section of code was for displaying more information towards the bottom of the webpage.

# The above section of code puts all that info. on a sidebar instead. 
 
# if st.checkbox("More info."):
#     st.write(d_text_2)
    
#     h_mich_img = PIL.Image.open('Hurricane Micheal.jpg')
#     cap_img = PIL.Image.open('CAP.jpg')
    
#     st.image(h_mich_img, use_column_width = True, caption = 'Hurricane Michael (as a category four storm) aftermath in the Florida Panhandle.')
#     st.image(cap_img, use_column_width = True, caption = 'CAP Pilot taking aerial photos of Hurricane Sandy.')
    
#     st.write(d_text_3)
    
#     map_image = PIL.Image.open('wildfire-activity-map-01.jpg')
#     st.image(map_image, use_column_width = True, caption = 'Wildfire Activity Map')
    
#     st.write('### Sources')
    
#     sources = PIL.Image.open('sources.jpg')
#     st.image(sources, use_column_width = True)


        
        