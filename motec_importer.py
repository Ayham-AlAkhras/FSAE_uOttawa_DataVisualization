# motec_importer.py

import os
import pandas as pd 
import numpy as np 


class MoTeCImporter:

    #Stores file path
    def __init__(self, path):

        self.path = path
        self.df = None

    #Loads the file, checks for errors, ignores certain info (such as comments in MoTeC), saves the file
    def load (self):

        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File not found: {self.path}")

        try:
            df = pd.read_csv(self.path, comment='#')

        except Exception as e:
            raise ValueError(f"Failed to load CSV: {e}")

        if df.empty:
            raise ValueError("CSV loaded, no data found")

        df = df.apply(pd.to_numeric, errors= "ignore")

        self.df = df

    #Validates to make sure it isn't all zero
    def validate_not_all_zero(self):

        numeric_df = self.df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            raise ValueError("No Numeric Data Found")

        if (numeric_df == 0).all().all():
            raise ValueError("All numeric values are 0.")

    #Validates to make sure sensors aren't frozen or logs are corrupted
    def validate_variation(self):

        numeric_df = self.df.select_dtypes(include=[np.number])

        if all(numeric_df[col].nunique() <= 1 for col in numeric_df.columns):
            raise ValueError("Channels show no variation.")

    def import_and_validate(self):

        self.load()
        self.validate_not_all_zero()
        self.validate_variation()

        print("MoTeC CSV Successfully Imported")
        print("\nPreview of data:")
        print(self.df.head(), "\n")

        return self.df

    def get_channel(self, name):

        if name not in self.df.columns:
            raise KeyError(f"Channel '{name}' not found.")

        return self.df[name]
