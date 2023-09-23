import re,sys,os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def getFileName():
    if getattr(sys,'frozen',False):
        return input("Enter your CSV name: ")
    else:
        return input("Enter your CSV name: ")

def checkDate(date_):
    pattern = r'\d{2}/\d{2}/\d{2}'
    return True if re.fullmatch(pattern,date_) else False

def setLine(given_line,earnings_temp):
    custom_row =[]
    
    if re.match(docket_pattern, given_line[0]):
        None
    elif checkDate(given_line[0]):
        given_line.insert(0,earnings_temp[0][0])
    else:     
        given_line.insert(0,earnings_temp[0][1])
        given_line.insert(0,earnings_temp[0][0])
               
    if len(given_line) == 10:
        custom_row.extend(given_line[:5]) 
    else:
        custom_row.extend(given_line[:4]) 
        
    numeric_part, *character_parts = given_line[-5].split()
    custom_row.extend([numeric_part, ' '.join(character_parts)]) 
    custom_row.extend(given_line[-4:])
    if len(custom_row) == 10:
        custom_row.insert(4,'')
    return custom_row

def appendToCsv(given_list,file_name,folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    res = ''
    for i in given_list:
        for j in i:
            j[3] = j[3].replace(',',' ')
            for k in j:
                res = res + ',' + k 
            res = res + ',' + truckNo
            res += '\n'
            
            with open(folder_name+'/'+file_name,'a') as f:
                f.write(res[1:])
                f.close()
                res = ''

# file_path = getFileName()
args = sys.argv[-1]

file_path = 'pdf.csv'

while(file_path[-4:] != '.csv'):
    print("Your given file is not valid.")
    file_path = getFileName()

converted_file = "converted_"+file_path

folderName =  file_path[:-4] + '_' + datetime.now().strftime("%d-%m-%Y%H%M%S")

earnings_carter_list, earnings_temp, earnings_flag, expense_flag, key, earnings_carter_dic = [], [], False, False, None, {}

carter_no = r'(\d+)\s+Truck\s+(\w+)'
docket_pattern = r'^\d{8}$|^\d{6}$'

with open(file_path, 'r') as file:
    for line in file:   
        if re.search(carter_no, line.replace(",",'').replace('Carter No:','').replace('"','').strip()):
            if earnings_carter_list != None and key != None and earnings_carter_list != []:
                earnings_carter_list.append(earnings_temp)
                earnings_temp = []
                earnings_carter_dic[truckNo] = earnings_carter_list
                # Appending into csv
                appendToCsv(earnings_carter_list,converted_file,folderName)  
                        
                earnings_carter_list = []
                earnings_flag = False
                
            key = line.replace('Carter No:','').replace('"','').strip()
            truckNo = key.split(',')[1] 
            truckNo = truckNo.split()[-1]
        else:
            line_split_temp_ = re.split(r'\s{2,}', line)
            line_split_temp_[0],line_split_temp_[-1] = line_split_temp_[0][1:],line_split_temp_[-1][:-2]
            
            try:
                if line_split_temp_[0].lower() != 'docket' and line_split_temp_[0].lower() != 'no.':
                    if re.match(docket_pattern, line_split_temp_[0]):
                        if earnings_temp:
                            earnings_carter_list.append(earnings_temp)
                            earnings_temp = []
                        line_split_temp_ = setLine(line_split_temp_,earnings_temp)
                        earnings_temp.append(line_split_temp_)
                    else:
                        if line_split_temp_[0].lower() not in ('"earnings', '"expenses', '"') and len(line_split_temp_) <= 1 and earnings_flag == True and re.match(r'^(?!"(po box|page)).*',line_split_temp_[0].lower()):    
                            earnings_temp[-1][3] = earnings_temp[-1][3] + line_split_temp_[0].replace('"',' ')
                            continue
                        elif line_split_temp_[0].lower() == '"earnings':
                            earnings_flag = True
                            expense_flag = False
                            continue
                        elif line_split_temp_[0].lower() == '"expenses':
                            earnings_flag = False
                            expense_flag = True
                            continue

                        if line_split_temp_[0].lower() == 'total earnings':
                            earnings_carter_list.append(earnings_temp)
                            earnings_temp = []
                            earnings_carter_dic[truckNo] = earnings_carter_list
                            # Appending into csv
                            appendToCsv(earnings_carter_list,converted_file,folderName)
                               
                            earnings_carter_list = []
                            earnings_flag = False 
                            key = None
                        elif len(line_split_temp_) >= 7 and line_split_temp_[0].lower() != 'earnings':
                            if earnings_flag == True:
                                line_split_temp_ = setLine(line_split_temp_,earnings_temp)
                                earnings_temp.append(line_split_temp_)
            except Exception as e:
                print(f'{e} at {line}')
                pass


