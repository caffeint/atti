from openai import OpenAI
import os
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

client = OpenAI()

file_upload = client.files.create(
  file=open("train.jsonl", "rb"),
  purpose="fine-tune"
)


client.fine_tuning.jobs.create(
  training_file=file_upload.id, 
  model="gpt-3.5-turbo",
  suffix="kimnami-babo"
)
