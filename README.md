# PM5560
 
The DeviceLogExport file listens on HTTP (443) port to receive the data log from the meter’s webpage and store it based on the scheduled time frequency in the server path for the meter. Please make sure that the DeviceLogExport.exe file is running so that port 443 is listening.

Once port 443 will receive an export it will save in DeviceLogs folder.

The datascript.py file will read the recently exported .csv file based on Date modified into a Pandas DataFrame. Using Pandas DataFrame, it will then convert the data values into the correct format. It will then export this correctly formatted data values into the Postgres. 

The graphscript.py file will fetch the data from the Postgres and store it in Pandas DataFrame. Using the Pandas DataFrame, it will then plot the graphs.   
 
