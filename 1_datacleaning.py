""" Intended to clean and preprocess the data, pulling from i_landing_layer and putting out into ii_raw_layer """

# Imports
from pathlib import Path

# 
print("Identified files:")
for f in Path("i_landing_layer/match_stats").iterdir():
    if f.is_file():
        print("> " + f.name)