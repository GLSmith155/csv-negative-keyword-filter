import re
import pandas as pd
import time
import numpy as np
import csv
import os

start = time.time()

# Place file name here with .csv, then run the script.
your_file_name = '3_1_2021_fr_replaced_matched_.csv'
updated_file_name = your_file_name[:-4] + '_unfiltered.csv'

# Columns to be scanned. NOTE: Column names should match the name used in the library.
# If column names change make necessary edits to library
columns_to_scan = ['Full Name', 'Current Position', 'Job Title', 'Company', 'Location', 'Description']

# Sets pos/neg library Keyword to first item in columns_to_scan. For-Loop iterates through.
Keyword = columns_to_scan[0]

# List of file names for .to_csv in the for-loop to reference
file_output = [your_file_name, updated_file_name]

#match_column_list = ['Match 1', 'Match 2', 'Match 3', 'Match 4', 'Match 5', 'Match 6', 'Match 7', 'Match 8', 'Match 9', 'Match 10', 'Match 11', 'Match 12', 'Match 13', 'Match 14', 'Match 15', 'Match 16', 'Match 17', 'Match 18', 'Match 19', 'Match 20', 'Match 21', 'Match 22', 'Match 23', 'Match 24', 'Match 25', 'Match 26']


def pos_neg_filter():

    data = pd.read_csv(file_name, engine = 'python', error_bad_lines = False)
    
    #for column_checker in range(26):
      #  p = column_checker
        
      #  if match_column_list[column_checker] in data:
      #      print(match_column_list[column_checker])
            
      #  else:
       #     data[match_column_list[column_checker]] = None
        
   # data.rename(columns={"A": "URL", "B": "Current Position", "C": "Job Title", "D": "Full Name", "E": "First Name", "F": "Surname", "G": "Company", "H": "Location", "I": "City", "J": "State", "K": "Country", "L": "Description", "M": "Match 1", "N": "Match 2", "O": "Match 3", "P": "Match 4", "Q": "Match 5", "R": "Match 6", "S": "Match 7", "T": "Match 8", "U": "Match 9", "V": "Match 10", "W": "Match 11", "X": "Match 12", "Y": "Match 13", "Z": "Match 14", "AA": "Match 15", "AB": "Match 16", "AC": "Match 17", "AD": "Match 18", "AE": "Match 19", "AF": "Match 20", "AG": "Match 21", "AH": "Match 22", "AI": "Match 23", "AJ": "Match 24", "AK": "Match 25", "AL": "Match 26"})
    

# columns_to_scan in the next 6 lines of code is searching the library for the current column name.
    pos = pd.read_csv('positive.csv').dropna(subset=[Keyword])
    neg = pd.read_csv('negative.csv').dropna(subset=[Keyword])

    pos_keys = pos.get(Keyword).tolist()
    pos_keys = [item.lower().strip() for item in pos_keys]

    neg_keys = neg.get(Keyword).tolist()
    neg_keys = [item.lower().strip() for item in neg_keys]


    #it_keys = ['it ', ' it', ' it '] #Get IT titles
    
    #pos_keys.append('it ')
    #pos_keys.append(' it')
    #pos_keys.append(' it ')

    #pos_keys.append('cto ')
    #pos_keys.append(' cto')
    #pos_keys.append(' cto ')

    pp = "|".join(pos_keys)
    nn = "|".join(neg_keys)
    
    df = data
    
    try:
    # If all subsets listed are empty, drop row. Only runs on first loop.
        if loop_number == 0:
    # The first column number equals match 1, the second number should surpass the total needed just in case.
            ix = df.loc[:, 'Match 1':].dropna(how='all').index.tolist()
            df = df.loc[ix]
    except:
        if loop_number == 0:
    # The first column number equals match 1, the second number should surpass the total needed just in case.
            ix = df.loc[:, 'Description':].dropna(how='all').index.tolist()
            df = df.loc[ix]        
    
    # specified_column_1 = column_to_filter #CHANGE SPECIFIED COLUMN HEADER FOR FILTER
    df = df.dropna(subset=[column_to_filter])    
 
    pos_index = []
    neg_index = []

    for col in df[column_to_filter].iteritems():
        pattern = re.compile(pp)
        stri = col[1].lower()
        find_pat = pattern.findall(stri,0,len(stri))
        if len(find_pat) >= 1:
            pos_index.append(col[0])

    df1 = df.loc[pos_index]
    
    for col in df1[column_to_filter].iteritems():
        pattern = re.compile(nn)
        stri = col[1].lower()
        find_pat = pattern.findall(stri,0,len(stri))
        if len(find_pat) >= 1:
            neg_index.append(col[0])
            
    global output_1        
    output_1 = df1.drop(index = neg_index)
    global unfiltered
    unfiltered = df.drop(index = output_1.index)
    
    
# _____________________ Loops for function, columns, and keywords _______________________________   

if __name__ == "__main__":    
# Loops through the function and column list. 
# Range(#) where # is equal to the number of columns to filter.
    for loop_filt in range(6):
        global loop_number
        loop_number = loop_filt

# Uses for-loop range to move through columns
        column_to_filter = columns_to_scan[loop_number]
# Uses for-loop range to move through columns and uses it for the current library Keyword
        Keyword = columns_to_scan[loop_number]
        
# Determines correct file_name to use from the file_output list.
        if loop_number == 0:
            file_name = file_output[0]
                      
        else:
            file_name = file_output[1]
            
        # Calls the filter function     
        pos_neg_filter()
        
# If this is the first loop with your_file_name, then 'if' creates a filtered and unfiltered csv.
        if file_name == your_file_name: 
            unfiltered_name = file_name[:-4] + '_unfiltered.csv'
            filtered_name = file_name[:-4] + '_filtered.csv'
            output_1.to_csv(filtered_name, mode="a", index = False)
            unfiltered.to_csv(unfiltered_name, mode="w", index = False)
            file_name = updated_file_name
            print('\'' + column_to_filter + '\' filtered.')
            time.sleep(3)
# Else we'll add the newly filtered data into the appropriate csv as they already exist from the 1st loop
        else:
            unfiltered_name = file_name
            unfiltered.to_csv(unfiltered_name, mode="w", index = False)
            filtered_name = file_name[:-15] + '_filtered.csv'
            output_1.to_csv(filtered_name, mode="a", index = False)
            print('\'' + column_to_filter + '\' filtered.')
            time.sleep(3)
            

end = time.time()
process_time = end - start
print('\nTime it took for script to run : {0}'.format(process_time))      
