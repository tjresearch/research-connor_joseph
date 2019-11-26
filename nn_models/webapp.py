import streamlit as st
import pandas as pd
import numpy as np 

from PIL import Image
import requests
from io import BytesIO
import torch
from fastai.vision import *
import csv





# @st.cache
# def load_data(nrows):    # nrows is number of rows it will read.
#     data = pd.read_csv("annotations_earthquake.csv", nrows=nrows)
#     return data


st.title("Autotations")

url = st.text_input("Link to Image")
st.write(url)

def user_image():
    try:
        data = requests.get(url)
        img = BytesIO(data.content)
        return img

    except:
        return None

@st.cache
def predictImg(img):
    img = open_image(img)
    path = Path(".")
    defaults.device = torch.device('cpu')
    learn = load_learner(path, "Joseph_Model_1.pkl")
    pred_class,pred_idx,outputs = learn.predict(img)
    return pred_class


img = user_image()
if img != None:
    st.image(PIL.Image.open(img))
    p_c = predictImg(img)
    st.write(p_c)
    st.write("Was I wrong?")
    if st.checkbox("Yes! Do better!"):
        dtype = st.radio("Which Disaster is in the Picture?", ["earthquake", "hurricane", "fire", "flooding", "normal"])
        if st.button("Confirm"):
            filename = dtype + "_urls.csv"
            with open(filename, "a") as fd:
                writer = csv.writer(fd)
                writer.writerow([url])
            st.write("Pushing this button more than once will append its url to the dataset more than once.")
            st.write("Unless you want this to happen, please don't push again.")
        