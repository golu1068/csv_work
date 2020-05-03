import pandas as pd
import math, time
import os
from tkinter import Tk, Button, Entry, Label, END
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import re
##########################################################################
def date2WN(year, month, day, hour, min, sec):
    secsInWeek = 604800   #  number of sec in a week
    secsInDay = 86400
    gpsEpoch = (1980, 1,6, 0, 0, 0)  # gps epoch for gps week number(6 jan,1980) 
    secFract = sec%1 
    epochTuple = gpsEpoch + (-1, -1, 0) 
    t0 = time.mktime(epochTuple) 
    t = time.mktime((year, month, day, hour, min, int(sec), -1, -1, 0))  
    tdiff = t - t0 
    gpsSOW = (tdiff % secsInWeek) + secFract 
    gpsWeek = int(math.floor(tdiff/secsInWeek)) 
    gpsDay = int(math.floor(gpsSOW/secsInDay)) 
    gpsSOD = (gpsSOW % secsInDay) 
    return (gpsWeek, int(gpsSOW), gpsDay, gpsSOD)
#################################################################################
def str_month2int_month(month):
    month_dictionary = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,'SEP':9,'OCT':10,'NOV':11,'DEC':12} 
    value = month_dictionary[month]
    return value
############################################################################
def telnet_val(data, telnet_value):
    while 1:
        value_name=''
        line = telnet_value.readline()
        if (line == ''):
            break
        line_list = line.split()
        for i in range(len(line_list)):
            if (line_list[i] != '='):
                value_name = value_name + line_list[i] + ' '
            else:
                value_name = value_name[:-1]
                break
        for j in range(len(data)):
            if (data[j] == value_name):
                data[j] = line_list[i+1]
    telnet_value.seek(0,0)
    return data 
#####################################################################   
################################################################################
def lat(value):
#    1deg = 60' = 3600"      to convert into degree
    value = float(value[0:2]) + float(value[3:5])*(1/60) + float(value[6:11])*(1/3600)
    return (value)    
def long(value):
    value = float(value[0:3]) + float(value[4:6])*(1/60) + float(value[7:12])*(1/3600) 
    return (value)     
############################################################################
def IRNSSL5_IRNSSS(txt_file, telnet_value): 
    header_l5=[];header_r=[];data_l5=[];a=1;
    header = ['PRN', 'C/N0', 'Track status', 'Iono type']  
    while 1:
        line = txt_file.readline()
        if (line == '\n'):
            continue
        if (line[0:7] == 'Channel'):
            continue
        if (line[0:8] == 'IRNSS S1'):
            break
        data_list = line.split()        
        if (int(data_list[0]) == a):
            for i in range(len(header)):
                header_r.append(header[i] + '_' + str(data_list[0]))
            header_l5 = header_l5 + header_r
            del data_list[0:1]
            data_l5 = data_l5 + data_list
            header_r=[] 
            a = a+1
            continue
        a=a+1
    ############ for IRNSS S1
    a=1;header_r=[];header_s1=[];data_s1=[]   
    while 1:        
        line = txt_file.readline()
        if (line == '\n'):
            continue
        if (line[0:7] == 'Channel'):
            continue
        if (line[0:3] == 'GPS'):
            break
        if (line[0:9] == '>NTP INFO'):
            data_l5 = telnet_val(data_l5, telnet_value) 
            data_s1 = telnet_val(data_s1, telnet_value)
            return (data_l5, header_l5, data_s1, header_s1,[],[],[],[],[],[])
        
        data_list = line.split()
        if (int(data_list[0]) == a):            
            for i in range(len(header)):
                header_r.append(header[i] + '_' + str(a))
            header_s1 = header_s1 + header_r
            del data_list[0:1]
            data_s1 = data_s1 + data_list
            header_r=[]
            a=a+1
            continue
        a=a+1
    ############### for GPS
    a=1;header_r=[];header_gps=[];data_gps=[]
    while 1:
        line = txt_file.readline()
        if (line == '\n'):
            continue
        if (line[0:7] == 'Channel'):
            continue
        if (line[0:4] == 'SBAS'):
            break

        data_list = line.split()
        if (int(data_list[0]) == a):            
            for i in range(len(header)):
                header_r.append(header[i] + '_' + str(a))
            header_gps = header_gps + header_r
            del data_list[0:1]
            data_gps = data_gps + data_list
            header_r=[]
            a=a+1
            continue
        a=a+1
    ################ for SBAS
    a=1;header_r=[];header_sbas=[];data_sbas=[]
    while 1:
        line = txt_file.readline()
        if (line == '\n'):
            continue
        if (line[0:7] == 'Channel'):
            continue
        if (line[0:7] == 'GLONASS'):
            break

        data_list = line.split()
        if (int(data_list[0]) == a):            
            for i in range(len(header)):
                header_r.append(header[i] + '_' + str(a))
            header_sbas = header_sbas + header_r
            del data_list[0:1]
            data_sbas = data_sbas + data_list
            header_r=[]
            a=a+1
            continue
        a=a+1
    ################# for GLONASS
    a=1;header_r=[];header_glonass=[];data_glonass=[]
    while 1:
        line = txt_file.readline()
        if (line == '\n'):
            continue
        if (line[0:7] == 'Channel'):
            continue
        if (line[0:9] == '>NTP INFO'):
            break

        data_list = line.split()
        if (int(data_list[0]) == a):            
            for i in range(len(header)):
                header_r.append(header[i] + '_' + str(a))
            header_glonass = header_glonass + header_r
            del data_list[0:1]
            data_glonass = data_glonass + data_list
            header_r=[]
            a=a+1
            continue
        a=a+1
    
    data_l5 = telnet_val(data_l5, telnet_value) 
    data_s1 = telnet_val(data_s1, telnet_value)
    data_gps = telnet_val(data_gps, telnet_value) 
    data_sbas = telnet_val(data_sbas, telnet_value)
    data_glonass = telnet_val(data_glonass, telnet_value)
    return (data_l5, header_l5, data_s1, header_s1, data_gps, header_gps, data_sbas, header_sbas, data_glonass, header_glonass)
##########################################################################
def file_write(file_path, file_name):
#    master.destroy()
#    master.withdraw()
    print('\nProcess started')
    telnet_value_file = 'telnet_value.txt'
    
    txt_file = open(os.path.join(file_path, file_name),'r')
    telnet_value = open(os.path.join(file_path, telnet_value_file), 'r')
    
    header = [];data=[];final_val=[];header_l5=[];final_data_l5=[];final_data_s1=[];final_data_gps=[];final_data_sbas=[];
    block=1;final_data_glonass=[];
    while 1:    
        line = txt_file.readline()    
        if (line == ""):
            break
        if (line[0:12] == "------------"):
            if (len(data) == 0):
                continue
            data = telnet_val(data, telnet_value)
            final_val.append(data)  
            if (len(data) > 131):
                print(data[0])
            data=[]
            header=[]
            block = block + 1       
            continue
        if (line[0:6] == 'Family'):
            location = line.find(':')
            filename_1 = line[location+1:][0:-1]
            for i in range(len(filename_1)):
                if (filename_1[i:i+1] == "\t" or filename_1[i:i+1] == ' '):
                    filename_1 = filename_1[i+1:]
            continue
        if (line[0:9] == 'Serial no'):
            location = line.find(':') 
            filename_2 = (line[location+1:][0:-1])
            for i in range(len(filename_2)):
                if (filename_2[i:i+1] == "\t" or filename_2[i:i+1] == ' '):
                    filename_2 = filename_2[i+1:]
            continue
        if (line[:][:-1] == 'IRNSS L5'):
             data_l5, header_l5, data_s1, header_s1, data_gps, header_gps, data_sbas, header_sbas,\
             data_glonass, header_glonass= IRNSSL5_IRNSSS(txt_file, telnet_value)
             data_l5[0:0] = [complete_date, WN, TOWC]
             data_s1[0:0] = [complete_date, WN, TOWC]
             data_gps[0:0] = [complete_date, WN, TOWC]
             data_sbas[0:0] = [complete_date, WN, TOWC]
             data_glonass[0:0] = [complete_date, WN, TOWC]            
             header_l5[0:0] = ['UTC', 'WN', 'TOWC']
             header_s1[0:0] = ['UTC', 'WN', 'TOWC']
             header_gps[0:0] = ['UTC', 'WN', 'TOWC']
             header_sbas[0:0] = ['UTC', 'WN', 'TOWC']
             header_glonass[0:0] = ['UTC', 'WN', 'TOWC']
             final_data_l5.append(data_l5)
             final_data_s1.append(data_s1)
             final_data_gps.append(data_gps)
             final_data_sbas.append(data_sbas)
             final_data_glonass.append(data_glonass)
             for i in range(len(header_l5)):
                 if (header_l5[i][0:4] == 'C/N0'):
                     header_l5[i] = header_l5[i] + ' (dB-Hz)'
             for i in range(len(header_s1)):
                  if (header_s1[i][0:4] == 'C/N0'):
                      header_s1[i] = header_s1[i] + ' (dB-Hz)' 
             for i in range(len(header_gps)):
                  if (header_gps[i][0:4] == 'C/N0'):
                      header_gps[i] = header_gps[i] + ' (dB-Hz)'
             for i in range(len(header_sbas)):
                  if (header_sbas[i][0:4] == 'C/N0'):
                      header_sbas[i] = header_sbas[i] + ' (dB-Hz)'
             for i in range(len(header_glonass)):
                  if (header_glonass[i][0:4] == 'C/N0'):
                      header_glonass[i] = header_glonass[i] + ' (dB-Hz)'           
                
        if (line.find(':') != -1):
            if (len(data) == 0 and line[0:3] != 'UTC'):
                continue
            location = line.find(':')
            if (line[0:3] == 'UTC' and line[3:4] == ':'):
                value = line[location+1:]
                R = len(value)
                for i in range(R):
                    j=0
                    if ('\n' in value):
                        value = value[:-1]               
                    if (value[j:j+1] == ' ' and value[j+1] == ' '):
                        value = value[j+1:]
                t = value[8:16]     #  time
                year = value[17:21]     
                month = (value[1:4])
                mon = str_month2int_month(month) 
                day = value[5:7]
                hour = value[8:10]
                minute = value[11:13]
                second = value[14:16] 
                WN, TOWC, gpsday, gpsSOD = date2WN(int(year), (mon),int(day),int(hour),int(minute),int(second))
                header.append('UTC')
                complete_date = month +' ' + day +' ' + year +' ' + t
                data.append(month +' ' + day +' ' + year +' ' + t)
                header.append('WN')
                header.append('TOWC')
                data.append(WN)
                data.append(TOWC)   
                while 1:
                    line = txt_file.readline() 
                    if (line[0:1] == '>'):
                        break
                continue        
            
            #####################################################################################
            value = line[location+1:]
            R = len(value)
            for i in range(R):
                j=0
                if ('\n' in value):
                    value = value[:-1]  
                if (value[j:j+1] == "\t" or value[j:j+1] == ' '):
                    value = value[j+1:]
                if (value[j:j+1] == ' '):
                    value = value[j+1:]             
            ###################################################################################
            name = line[0:location+1]          
            i = -1
            for rand in range(len(name)):   
                i = i + 1
                if (name[i:i+1] == "\t" and name[i+1] == ':'):
                    name = name[:i] + '' + name[i+1:]
                    i = i - 1
                if (name[i:i+1] == ' ' and (name[i+1] == ':' or name[i+1] == ' ')):
                    name = name[:i] + '' + name[i+1:]
                    i = i - 1
                if (name[i:i+1] == ':'):
                    name = name[:i] + name[i+1:]
            if (name == 'LAN1 IP'):
                value_list = value.split('.')
                ip = value_list[3]
            if (value[-4:] == ' sec'):
                header.append(name[:] + ' (sec)' )
                data.append(value[:-4])
            elif (value[-3:] == ' ns'):
                header.append(name[:] + ' (ns)' )
                data.append(value[:-3])
            elif (value[-2:] == ' m'):
                header.append(name[:] + ' (m)' )
                data.append(value[:-2])
            elif (value[-5:] == ' Gbps'):
                header.append(name[:] + ' (Gbps)' )
                data.append(value[:-5])
            elif (value[-6:] == ' volts'):
                header.append(name[:] + ' (volts)' )
                data.append(value[:-6])
            elif (value[-5:] == ' msec'):
                header.append(name[:] + ' (msec)' )
                data.append(value[:-5])
            elif (value[-5:] == ' hour'):
                header.append(name[:] + ' (hour)' )
                data.append(value[:-5])
            elif (value[3:7] == 'hour' and value[11:14] == 'min'):
                header.append(name[:] + ' (hour:min)' )
                data.append(value[0:2] + ':' + value[8:10])
            elif (name[0:8] == 'Latitude'):
                direction = value[-1:]
                value = lat(value)
                header.append(name + ' (degree)')
                data.append(str(value) + ' ' + direction)
            elif (name[0:9] == 'Longitude'):
                direction = value[-1:]
                value = long(value)
                header.append(name + ' (degree)')
                data.append(str(value) + ' ' + direction)
            else:
                header.append(name[:])  
                data.append(value[:])    
                
    data = telnet_val(data, telnet_value)                    
    final_val.append(data)
    print('Total number of block of data= ',block)
    
    csv_filename = filename_1 + '__' + filename_2 + '_' + ip + '.csv'
    file_write = open(os.path.join(file_path, csv_filename), 'w', newline='')
    df = pd.DataFrame(final_val, columns= header)   
    df.to_csv(file_write, index=False)
    file_write.close()
    
    csv_filename_l5 = filename_1 + '__' + filename_2 + '_L5_' + ip + '.csv'
    file_write_l5 = open(os.path.join(file_path, csv_filename_l5), 'w', newline='')
    df1 = pd.DataFrame(final_data_l5, columns= header_l5)   
    df1.to_csv(file_write_l5, index=False)
    file_write_l5.close()
    
    csv_filename_S1 = filename_1 + '__' + filename_2 + '_S1_' + ip + '.csv'
    file_write_s1 = open(os.path.join(file_path, csv_filename_S1), 'w', newline='')
    df2 = pd.DataFrame(final_data_s1, columns= header_s1)   
    df2.to_csv(file_write_s1, index=False)
    file_write_s1.close()
    
    if (len(header_gps) > 3):
        csv_filename_gps = filename_1 + '__' + filename_2 + '_gps_' + ip + '.csv'
        file_write_gps = open(os.path.join(file_path, csv_filename_gps), 'w', newline='')
        df3 = pd.DataFrame(final_data_gps, columns= header_gps)   
        df3.to_csv(file_write_gps, index=False)
        file_write_gps.close()
    
    if (len(header_sbas) > 3):
        csv_filename_sbas = filename_1 + '__' + filename_2 + '_sbas_' + ip + '.csv'
        file_write_sbas = open(os.path.join(file_path, csv_filename_sbas), 'w', newline='')
        df4 = pd.DataFrame(final_data_sbas, columns= header_sbas)   
        df4.to_csv(file_write_sbas, index=False)
        file_write_sbas.close()
    
    if (len(header_glonass) > 3):
        csv_filename_glonass = filename_1 + '__' + filename_2 + '_glonass_' + ip + '.csv'
        file_write_glonass = open(os.path.join(file_path, csv_filename_glonass), 'w', newline='')
        df5 = pd.DataFrame(final_data_glonass, columns= header_glonass)   
        df5.to_csv(file_write_glonass, index=False)
        file_write_glonass.close()
######################################################################################
    #  To plot the difference of TSPO
    parameter_search = e2.get()
    if (parameter_search != ''):                
        diff_parameter_list =[];
        file = os.path.join(file_path, csv_filename)
        file_df = pd.read_csv(file, low_memory=False)
        
#        header_list = list(file_df.columns.values)   # to get the header as list
        header_list = list(file_df)         # to get the header as list
        for i in range(len(header_list)):           
            parameter_name = header_list[i]
    #        if (parameter_name.find(parameter_search) != -1):
            if (re.search(parameter_search, parameter_name, re.IGNORECASE)):
                parameter = parameter_name
                break
        try:            
            parameter_list = file_df[parameter]   
            msg.config(text='',bg='SystemButtonFace')    
            #msg.update_idletasks()            
        except:      
            msg.config(text = 'Please enter a \n valid parameter',bg='red')
            #msg.update_idletasks()
            telnet_value.close()
            file_write_l5.close()
            file_write_s1.close()
            return 
        for i in range(len(parameter_list)-1):
            diff_parameter_value = parameter_list[i+1] - parameter_list[i]
            diff_parameter_list.append(diff_parameter_value)
            if (diff_parameter_value != 1):
                print('index= %d'%(i+2) , '   ', 'difference= %d'%(diff_parameter_value))
        plt.figure(1)
        plt.subplot(211)
        plt.title('Plot of values')
        plt.plot(parameter_list)   
        plt.subplot(212)
        plt.title('Plot for difference of values')
        plt.plot(diff_parameter_list)
        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.40,
                        wspace=.35)
#####################################################################################
    telnet_value.close()
    txt_file.close()
    return 1
##############################################################################################
def browse_filepath():
    e1.delete(0,END)
    dir_path = askopenfilename(initialdir='')
    e1.insert(10, dir_path)

def goto_submit():
#    master.withdraw()
    file_path = e1.get()
    file_path_list = file_path.split('/')
    file_name= file_path_list[-1:][0]
    file_path_len = len(file_path) - len(file_name) -1
    file_path = file_path[:file_path_len]
    return_value = file_write(file_path, file_name)
    if (return_value == 1):
        print('Process completed')
    else:
        pass
#    master.deiconify()                         #  To display the window
       
master = Tk()
master.geometry('300x100+500+400')
#master.attributes('-fullscreen', True)
master.title('telnet')
#q=master.cget('bg')    # important

#w, h = master.winfo_screenwidth(), master.winfo_screenheight()
##master.overrideredirect(1)
#master.geometry("%dx%d+0+0" % (w, h))
msg=Label(master)
msg.grid(row=1,column=2)

Label(master, text='Telnet file').grid(row=0, column=0, padx=0)
e1 = Entry(master)
e1.grid(row=0, column=1, sticky='w')

Label(master, text='Parameter').grid(row=1, column=0, padx=0)
e2 = Entry(master,width=15)
e2.grid(row=1, column=1, sticky='w',pady=10)
e2.insert(10,'TSPO')
b1 = Button(master, text='Browse', bg='light blue', command= browse_filepath)
b1.grid(row=0, column=2,padx=8)
b2 = Button(master, text='Submit', bg='light green', command=goto_submit)
b2.grid(row=2,column=1,pady=10)
b3 = Button(master, text='Quit', bg='red', command=master.destroy)
b3.grid(row=2,column=0)

master.mainloop()
