from multiapp import MultiApp
import streamlit as st
from enter_case import enter_text
from pdf import upload_file

app = MultiApp()
app.add_app("Enter the text of the case content", enter_text)
app.add_app("Upload the case file", upload_file)
app.run()
