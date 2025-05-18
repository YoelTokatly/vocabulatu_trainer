# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

from functions import  Functions
from start import initial_db
import json
import polars as pl
from constant import FILE_PATH
from constant import DB_PATH
# import pandas as pd
# my_functions = Functions()


def main():
    print("Hello from vocabulatu-trainer!")
    initial_db(FILE_PATH,DB_PATH)
    mode=input("choose mode 'e' for edit, 't' for Training or 'q' for Testing").lower().strip()
    file_name = 'vocab_hebrew.json'
    if mode == 'e':
                Functions.edit(DB_PATH) 
    elif mode == 't':
        Functions.traning(DB_PATH)
    elif mode == 'q':
        Functions.testing()
    else :
        mode=input("choose mode 'e' for edit, 't' for Training or 'q' for Testing").lower().strip()


if __name__ == "__main__":
    main()

