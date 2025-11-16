#!/usr/bin/env python
import sys
import os

# Write output to file instead of stdout
output_file = open('test_output.txt', 'w')

try:
    output_file.write("Python started\n")
    output_file.flush()
    
    output_file.write("Importing pandas...\n")
    output_file.flush()
    import pandas as pd
    output_file.write("Pandas imported successfully\n")
    output_file.flush()
    
    output_file.write("Loading CSV...\n")
    output_file.flush()
    df = pd.read_csv('../energydata_complete.csv')
    output_file.write(f"CSV loaded: {len(df)} rows, {len(df.columns)} columns\n")
    output_file.flush()
    
    output_file.write("Importing flask...\n")
    output_file.flush()
    from flask import Flask
    output_file.write("Flask imported successfully\n")
    output_file.flush()
    
    output_file.write("All imports successful! Ready to run app.py\n")
    output_file.flush()
    
except Exception as e:
    output_file.write(f"ERROR: {str(e)}\n")
    output_file.flush()
    import traceback
    traceback.print_exc(file=output_file)
    output_file.flush()
finally:
    output_file.close()
