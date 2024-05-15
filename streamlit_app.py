import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import os
from utils import *
import csv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_MODEL = os.getenv("CHAT_MODEL")
client = OpenAI(api_key=OPENAI_API_KEY)

uploaded_file = st.file_uploader("Choose a CSV file")
text_input = st.text_input(
    "Enter the word 👇"
)

# df = pd.read_csv("Definition 2024 04 23_result.csv")

# @st.cache
# def convert_df(df):
#     return df.to_csv().encode('utf-8')


# csv = convert_df(df)

# st.download_button(
#     "Press to Download",
#     csv,
#     "browser_visits.csv",
#     "text/csv",
#     key='browser-data'
# )


if uploaded_file is not None:
    
    dataframe = pd.read_excel(uploaded_file, sheet_name=None)
    dataframe = dataframe["Sheet1 (2)"]["Word"] 

    file_name = uploaded_file.name.split(".")[0] + "_result.csv"

    print("file_name: ", file_name)

    with open(file_name, 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        for data in dataframe:

            if not pd.isna(data):
                    
                    print("data: ", data)

                    response = client.chat.completions.create(
                        model=CHAT_MODEL,
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"Provide definitions of {data}"}
                        ]
                    )
    
                    result = response.choices[0].message.content
                    results = result.split("\n")
                    results.insert(0, data)
                    # results = ",".join(results) + "\n"

                    csvwriter.writerow(results)
    
    with open(file_name) as csvfile:                   
        st.download_button("Download final results", csvfile, file_name=file_name)
        

    
if text_input:

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Provide definitions of {text_input}"}
        ]
    )
    result = response.choices[0].message.content
    st.write(result)