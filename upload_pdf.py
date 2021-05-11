import pickle
import streamlit as st

def classify_utterance(utt):
    # load the vectorizer
    loaded_vectorizer = pickle.load(open('vectorizer1.pickle', 'rb'))

    # load the model
    loaded_model = pickle.load(open('classification1.model', 'rb'))

    # make a prediction
    return(loaded_model.predict(loaded_vectorizer.transform([utt])))

     

#st.title("First information Report")

#case_content = st.text_input("Case Content", "")

if st.button("Predict"):
        result = classify_utterance(case_content)

        st.success('The output is {}'.format(result))

from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import streamlit as st
import os
from google_trans_new import google_translator
pytesseract.pytesseract.tesseract_cmd = (
    r'/usr/bin/tesseract'
)
import csv
page_count = 0

def extract_text(file_path):
    PDF_file = file_path
    
    # Store all the pages of the PDF in a variable 
    pages = convert_from_path(PDF_file, 500) 

    images = []
    image_counter = 1
    all_t = ""
    # Iterate through all the pages stored above 
    for page in pages:
      filename = "page_" + str(image_counter) + ".jpg"
      page.save(filename, 'JPEG')
      images.append(filename)
      text = pytesseract.image_to_string(filename, lang="kan")
      all_t += text
      image_counter += 1

    FIR_starts = 0
    FIR_ends = 0
    counter = 0

    for line in all_t.splitlines():
      counter += 1
      if line.startswith('10. ಪ್ರಥಮ ವರ್ತಮಾನ ವರದಿಯ ವಿವರಗಳು'):
        FIR_starts = counter
      if 'ತೆಗೆದುಕೊಂಡ ಕ್ರಮ' in line:
        FIR_ends = counter
    FIR_content = (" ".join(all_t.strip("\n").splitlines()[FIR_starts - 1 : FIR_ends]))    
    for img in images:
        os.remove(img)
    return(FIR_content)


def translate_row(row):
    translator = google_translator()
    a = translator.translate(row, lang_tgt='en')
    index = a.find("Report")
    index2 = a.rfind("11")
    return a[index+6:index2]

uploaded_file = st.file_uploader("Upload Files",type='pdf')
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    kannada_text = (extract_text(uploaded_file.name))
    english_text = translate_row(kannada_text)
    st.write(english_text)
