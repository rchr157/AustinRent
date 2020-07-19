# Import modules
import pandas as pd
import os
import datetime
import time
import glob
import shutil

# Start Time:
start_time = time.time()

# Get directory
austin_directory = os.getcwd() + "\DataSource" + "\OGSB-Austin"

os.chdir(austin_directory)
# Get a list of all csv files
all_csv = [i for i in glob.glob('*.csv')]


# Master CSV files for Apartment Rent
master_details = 'Master_Details.csv'

# Repeat for Detail csv files

# Concatenate all detail files into a DataFrame
details_df = pd.concat([pd.read_csv(f) for f in all_csv], sort=False)  # concatenate all data
# details_df.drop(details_df.columns[0], axis=1, inplace=True)  # drop first column (index)
details_df = details_df.reset_index(drop=True)  # reset index
details_df = details_df.drop_duplicates(keep='first')

# Append Data to Master CSV file
if master_details in all_csv:
    # remove master csv file from list
    all_csv.remove(master_details)

    # Drop duplicates from Master csv file
    master_detail_df = pd.read_csv(master_details)
    new_details_df = pd.concat([master_detail_df, details_df], axis=0, sort=False)
    new_details_df = new_details_df.reset_index(drop=True)
    new_details_df = new_details_df.drop_duplicates(keep=False)
    # Add latest files to Master csv list:
    with open(master_details, 'a', encoding='utf-8') as f:
        new_details_df.to_csv(f, header=False, index=False)
else:
    # If Master file hasn't been created, add header
    with open(master_details, 'a', encoding='utf-8') as f:
        details_df.to_csv(f, header=True, index=False, line_terminator='\r')


print("Data_Combiner.py took {} seconds to run".format(time.time()-start_time))
