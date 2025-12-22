# motec_importer.py

import os
import pandas as pd 
import numpy as np 

class MoTeCImporter:

    def __init__(self, path):
        self.path = path            # Path to the CSV file
        self.raw = open(
            self.path, "r", 
            encoding="utf-8", 
            errors="ignore")
        self.df = None              # DataFrame to hold the loaded data
        self.metadata = {}          # Metadata that is located at the top of the csv files
        self.channels = {}          # Channel items with their units
        self.header_index = None    # Index of the header row
    
    def _find_header_index(self):
        """Finds the index of the header row starting with 'Time'."""
        
        target = '"Time"'
        encountered = False
        for i, line in enumerate(self.raw):
            if line.strip().startswith(target) and encountered is True:
                self.header_index = i
                return i
            elif line.strip().startswith(target):
                encountered = True
        raise ValueError('Could not find header row starting with "Time". Is this a RaceStudio CSV export?')


    def _fetch_metadata(self):
        """Extracts metadata from the top of the CSV file."""
        
        metadata = {}
        self.raw.seek(0)  # Reset file pointer to the beginning
        for i, line in enumerate(self.raw):
            if line.strip() == "":
                continue
            if i >= self.header_index - 1:
                break
            key, value = line.split(',', 1)
            metadata[key] = value
        self.metadata = metadata
    
    def load(self):
        """
        Loads the file, checks for errors, ignores certain 
        info (such as comments in MoTeC), saves the file
        """

        df = pd.read_csv(
            self.path, 
            skiprows=self._find_header_index(),
            )
        if df.empty:
            raise ValueError("CSV loaded, no data found")
        
        # First row after header is the units row
        units_row = df.iloc[0]
        self.channels = units_row.to_dict()

        # Drop units row from data and convert to numeric where possible
        df = df.iloc[1:].reset_index(drop=True)
        try:
            df = df.apply(pd.to_numeric)
        except Exception as e:
            raise ValueError(f"Error converting data to numeric: {e}")
        
        self._fetch_metadata()
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
