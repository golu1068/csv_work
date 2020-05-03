import pandas as pd
import numpy as np
import calendar
import os
from glob import glob

#file = r'/home/nagendra/python_code/freela/excel_file/Export_Output2007.csv'
#file_dir = os.path.split(file)[0]
#new_file = os.path.join(file_dir, 'new_file.csv')
#new_file = r'/home/nagendra/python_code/freela/excel_file/new_file_Export_Output2007.csv'
        
########################################################
def read_csv(file):
    day_sum=[];
    file_dir = os.path.split(file)[0]
    file_name = os.path.split(file)[1]
    
    new_file = os.path.join(file_dir, file_name[:-4]+ '_new_file.csv')
    write_file = open(new_file, 'w', newline='')
    
    df = pd.read_csv(file, low_memory=False)
    header = list(df)
    
    area = np.array(df['F_AREA'])
    area_sum = np.sum(area)
    
    weight = area/area_sum
    ######################################################
    year=2018
    if (calendar.isleap(year) == True):
        period = 366
    else:
        period = 365
    date = pd.date_range('01-01-'+str(year), periods=period)
    
    for i in range(3, 368):
        df[header[i]] = np.array(df[header[i]])*weight
        day_sum.append(np.sum(df[header[i]]))
    df.insert(len(header), 'Weight', weight)
    header = list(df)
    if (len(df) < len(day_sum)):
        df1 = pd.DataFrame(index=list(range(len(df), len(day_sum))))
        df = pd.concat([df, df1])
        df.fillna('')
        df.insert(len(header), 'Date', date)
        header = list(df)
        df.insert(len(header), 'Sum', day_sum)
    else:
        df['Date'] = pd.series(date)
        df['Sum'] = pd.series(day_sum)
        df.fillna('')
    
    df.to_csv(write_file, index=False)
    
    write_file.close()
#######################################
dir = os.getcwd()
os.chdir(dir)
files = glob('*.csv')
if (len(files) == 0):
    print('No any CSV file in this folder')
for file in files:
    if (file[-4:] == '.csv'):
        read_csv(file)
print('Conversion done')
input('Please press Enter key')
#######################################################################
#file_test = r'/home/nagendra/python_code/freela/excel_file/test.csv'
#write_file_test = r'/home/nagendra/python_code/freela/excel_file/write_test.csv'

#df = pd.read_csv(file_test, low_memory=False)
#he = list(df)
#for i in range(len(he)):
#    df[he[i]] = np.array(df[he[i]])*np.array([5,5,5])
#
#df.to_csv(write_file_test)
##################################################################

#a = [1,2,3]
#b = [5,6,7]
#c = [];
#c.append(a)
#c.append(b)
#header = ['a','b']
#
#header = np.transpose(header)
#
#df = pd.DataFrame(header)
#df.T.to_csv(write_file, index=False, mode='w', header=False)
#
#df = pd.DataFrame(c)
#data=[11,12,13]
#data1 = pd.DataFrame(data)
#df.append(data1, ignore_index=False,sort=False)
#df.to_csv(write_file, index=False, mode='a', header=False)
#
#write_file.close()
