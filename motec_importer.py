# motec_importer.py

import os
import pandas as pd 
import numpy as np 


class MoTeCImporter:

    #Stores file path
    def __init__(self, path):

        self.path = path
        self.df = None
        self.metadata = {} # Metadata that is located at the top of the csv files
        self.units = {}    # Units for each channel
    
    def _find_header_index(self):
        
        target = '"Time","GPS Speed","GPS Nsat","GPS LatAcc","GPS LonAcc","GPS Slope","GPS Heading","GPS Gyro","GPS Altitude","GPS PosAccuracy","GPS SpdAccuracy","GPS Radius","GPS Latitude","GPS Longitude"'
        
        with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if line.strip() == target:
                    return i
        raise ValueError('Could not find header row starting with "Time". Is this a RaceStudio CSV export?')

    #Loads the file, checks for errors, ignores certain info (such as comments in MoTeC), saves the file
    def load(self):

        header_index = self._find_header_index()
        df = pd.read_csv(self.path, skiprows=header_index)

        if df.empty:
            raise ValueError("CSV loaded, no data found")

        # First row after header is the units row
        units_row = df.iloc[0]
        self.units = units_row.to_dict()

        # Drop units row from data and convert to numeric where possible
        df = df.iloc[1:].reset_index(drop=True)
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

        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File not found: {self.path}")
        
        self.load()
        self.validate_not_all_zero()
        self.validate_variation()

        return self.df

    def get_channel(self, name):

        if name not in self.df.columns:
            raise KeyError(f"Channel '{name}' not found.")

        return self.df[name]
