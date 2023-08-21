# import os

# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))



import re

file_path = 'pdf.csv'
carter_dic = {}
carter_list = []
temp = []
key = None
# carter_no = r'^Carter No: (\d+), Truck (\d+\.\d+),[A-Z0-9]+$'
carter_no = r'(\d+)\s+Truck\s+(\w+)'
docket_pattern = r'^\d{8}$|^\d{6}$'

with open(file_path, 'r') as file:
    for line in file: 
               
        if re.search(carter_no, line.replace(",",'').replace('Carter No:','').replace('"','').strip()):
            if carter_list is not None and key is not None:
                carter_list.append(temp)
                temp = []
                carter_dic[key] = carter_list
                carter_dic[key] = carter_list
                carter_list = []
            key = line.replace(",",'').replace('Carter No:','').replace('"','').strip()
        else:
            
            line_split = line.split(',')
            line_split_temp_ = line_split[0].split() + line_split[1:]
            try:
                if re.match(docket_pattern, line_split_temp_[0]):
                    if temp:
                        carter_list.append(temp)
                        temp = []
                    temp.append(line_split_temp_)
                else:
                    if len(line_split_temp_) == 11 and line_split_temp_[0].lower() != 'earnings':
                        temp.append(line_split_temp_)
                    elif line_split_temp_[2].lower() == 'total earnings' or line_split_temp_[1].lower() =='delivery':
                        carter_list.append(temp)
                        temp = []
                        carter_dic[key] = carter_list
                        # carter_dic.values()
                        carter_list = []
                        key = None
            except:
                pass
# Print the resulting dictionary
for i in carter_dic:
    print(f"\n{i} :")
    for j in carter_dic[i]:
        print(j)