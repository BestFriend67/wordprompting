import pandas as pd

dataframe = pd.read_excel("E:\dev\gptweb\educational GPT\Definition 2024 04 23.xlsx", sheet_name=None)
dataframe = dataframe["Sheet1 (2)"]

for data in dataframe["Word"]:
    print(data)