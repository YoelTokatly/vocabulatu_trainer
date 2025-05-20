# /// script
# requires-python = ">=3.12"
# dependencies = [
# "pandas==2.2.3"]
# ///



from functions_st import  Functions
from start import initial_db
import json
# import polars as pl
from constant import FILE_PATH
from constant import DB_PATH
import pandas as pd
import sqlite3 
import streamlit as st
# my_functions = Functions()



# /// script
def main():
    st.title("Vocabulary Trainer")
    st.write("Welcome to the Vocabulary Trainer! This app helps you learn and practice vocabulary.")
    st.write("Choose a mode to get started from the left navigation bar.")

    st.sidebar.header("Choose Mode")
    mode = st.sidebar.radio("Select a mode:", ['Edit', 'Training', 'Testing'], index=None)

    if mode == 'Edit':
        st.write("Edit mode selected.")
        Functions.edit(DB_PATH)
    elif mode == 'Training':
        st.write("Training mode selected.")
        Functions.traning(DB_PATH)
    elif mode == 'Testing':
        st.write("Testing mode selected.")
        Functions.testing(DB_PATH)
    
    st.write("Thank you for using the Vocabulary Trainer!")
#     print("Hello from vocabulatu-trainer!")
#     initial_db(FILE_PATH,DB_PATH)
#     mode=input("choose mode 'e' for edit, 't' for Training or 'q' for Testing").lower().strip()
#     file_name = 'vocab_hebrew.json'
#     if mode == 'e':
#                 Functions.edit(DB_PATH) 
#     elif mode == 't':
#         Functions.traning(DB_PATH)
#     elif mode == 'q':
#         Functions.testing(DB_PATH)
#     else :
#         mode=input("choose mode 'e' for edit, 't' for Training or 'q' for Testing").lower().strip()


if __name__ == "__main__":
    main()

