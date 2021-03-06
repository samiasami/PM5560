##**********************************************************************************************************
#   Title: Data Script
#   Author: Samia Sami
#	Date: March 9, 2020
# 	Description: This program will read the recently exported .csv file based on Date modified into
# 	             a Pandas DataFrame. Using Pandas DataFrame, it will then convert the data values into 
# 	             the correct format. It will then export this correctly formatted data values into 
# 	             the Postgres.
##**********************************************************************************************************

import pandas as pd
import os
import glob
from sqlalchemy import create_engine
import datetime as dt
import numpy as np
import logging
logging.basicConfig(filename="test.log", level=logging.DEBUG,format="%(asctime)s:%(levelname)s:%(message)s")

#checks if port 433 is in use
import socket
def tryPort(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("0.0.0.0", port))
        result = True
    except:
        print("Port is in use.")
    sock.close()
    return result

tryPort(443)
#converts a number to binary
def float_bin(n): 
    s = bin(n & int("1"*32, 2))[2:]
    res=("{0:0>%s}" % (32)).format(s)
    return res   

def decimal_converter(num):   
    while num > 1:  
        num /= 10
    return num  

def frac (s, base):
    dotPos=s.find('.')
    if (dotPos == -1):
        return (int(s, base))
    places = len(s)-dotPos-1
    return (1.0*int(s[:dotPos]+s[dotPos+1:],base)/(base**places))

#converts the number from Float32 to Base 10
def IEEE754(n) : 
    
    if n < 0 : 
        sign = 1
        sign=1
    else:
        sign = 0

    list=[]
    if n % 1 == 0:
        whole = float_bin (n)
        whole=whole[1:]
        from decimal import Decimal
        exponent=whole[0:8]
        exponent=int(exponent,2)
        s=whole[8:31]
        for i in range(0, len(whole[8:31])):
            list.append(s[i])
        a=['.']
        b=['1']
        my_list=b+a+list
        mantissa="".join(str(x) for x in (b+a+list))
        mantissa=frac(str(mantissa),2)
        return (round(((-1)**sign) * (2**(exponent-127)*mantissa),3))

#Takes a Float32 array as an input and returns Base 10 array
def IEEE754_(array):
    mylist = []
    rows=array.shape[0]

    for i in range(rows):
       mylist.append(IEEE754((array)[i]))
    mat = np.array(mylist)
    return np.transpose([mat])

    
#converts the number from Int16 to Base 10      
def int16todecimal(n):
    whole = float_bin (n)
    whole=whole[2:]
    return(round(int(whole, 2),3))

#Takes a Int16 array as an input and returns Base 10 array
def int16_(array):
    mylist = []
    rows=array.shape[0]

    for i in range(rows):
       mylist.append(int16todecimal((array)[i]))
    mat = np.array(mylist)
    return np.transpose([mat])

#Power Factor conditions as per PM5560 Modbus Register List 
def valueabove1(n):
    PF_Val = 2 - n;
    return PF_Val

def valueless1(n):
    PF_Val = -2 - n;
    return PF_Val

def valueequal1(n):
    PF_Val = n;
    return PF_Val

def elsecase(n):
    PF_Val = n;
    return PF_Val


#Takes a raw power factor values array as an input and returns correct power factor array
def powerfactor(array):
    mylist = []
    rows=array.shape[0]


    for i in range(rows):
        value=(array)[i]
        if value[0]==-5.104235503814077e+38:
            mylist.append([0])
        elif value>1:
            mylist.append(valueabove1((array)[i]))
        elif value<(-1):
            mylist.append(valueless1((array)[i]))
        elif abs(value)==1:
            mylist.append(valueequal1((array)[i]))
        else:
            mylist.append(elsecase((array)[i]))

    
    return np.array(mylist)


#selects the latest file in the folder
try:
    folder = os.path.abspath(os.getcwd())
    list_of_files = glob.glob('*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    _, filename = os.path.split(latest_file)



    ## Preprocess the csv file and then insert new values of the latest export file to the existing table in memory sqlite database 
    from sqlalchemy.engine.url import URL
    engine = create_engine('postgresql://postgres:teampower@localhost:5436', paramstyle='format')
    df = pd.read_csv(filename,skiprows=7,usecols=range(2,17))
    logging.debug("File has been read and stored into the dataframe.")
    #converts the Float32 values of powerfactor to decimal base 10
    pf=IEEE754_(df['Power Factor Total'])


    #create a reformatted dataframe
    dataset=pd.DataFrame(np.concatenate((IEEE754_(df['Current Average'].to_numpy()),IEEE754_(df['Voltage B-C'].to_numpy()),IEEE754_(df['Voltage A-B'].to_numpy()),IEEE754_(df['Voltage L-L'].to_numpy()), IEEE754_(df['Active Power Total'].to_numpy()), IEEE754_(df['Apparent Power Total'].to_numpy()), IEEE754_(df['Reactive Power Total'].to_numpy()),
    int16_(df['Active Energy Delivered (KWh)'].to_numpy()),int16_(df['Active Energy Received (KWh)'].to_numpy()),int16_(df['Apparent Energy Delivered (KVAh)'].to_numpy()),powerfactor(pf), int16_(df['Apparent Energy Received (KVAh)'].to_numpy()),
    int16_(df['Reactive Energy Delivered (KVARh)'].to_numpy()), int16_(df['Reactive Energy Received (KVARh)'].to_numpy())), axis=1))
    dataset.columns = ['Current Average','Voltage B-C', 'Voltage A-B', 'Voltage L-L', 'Active Power Total', 'Apparent Power Total','Reactive Power Total','Active Energy Delivered (KWh)','Active Energy Received (KWh)','Apparent Energy Delivered (KVAh)',
                       'Power Factor Total', 'Apparent Energy Received (KVAh)','Reactive Energy Delivered (KVARh)','Reactive Energy Received (KVARh)'
                      ]

    horizontal_stack = pd.concat([df['Local Time Stamp'], dataset], axis=1)
    logging.debug("Dataframe is properly formatted to be loaded into the database.")

    #upload the dataframe on the database
    horizontal_stack.to_sql('meterdata', con=engine, if_exists='append',index=False)
    logging.debug("Dataframe successfully loaded into the database.")

except Exception as e:
    logging.error("Exception occurred", exc_info=True)
    logging.debug("Check to see if the port 443 is still listening. Check to see if the latest exported file is correctly exported.")
