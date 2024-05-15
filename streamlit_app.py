import streamlit as st
import pandas as pd
from openai import OpenAI
from utils import *
import csv


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
print(OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

uploaded_file = st.file_uploader("Choose a CSV file")
text_input = st.text_input(
    "Enter the word 👇"
)


if uploaded_file is not None:
    
    dataframe = pd.read_excel(uploaded_file, sheet_name=None)
    dataframe = dataframe["Sheet1"]["Word"] 

    file_name = uploaded_file.name.split(".")[0] + "_result.csv"

    print("file_name: ", file_name)

    with open(file_name, 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        for data in dataframe:

            if not pd.isna(data):
                    
                    print("data: ", data)

                    response = client.chat.completions.create(
                        model="gpt-4-0125-preview",
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
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Provide definitions of {text_input}"}
        ]
    )
    result = response.choices[0].message.content
    st.write(result)