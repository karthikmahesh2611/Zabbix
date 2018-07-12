# Created By: Karthik Mahesh
#Email: karthik224488@gmail.com

#Script to pull alert history report through zabbix API.
#This script will ask you to enter the 'from' and 'to' date&time in UNIX epoch format. 
#The result will be stored in a csv file having three fields "Date&Time" "HostName" "Alert Description"
import time
import json
import csv
from datetime import datetime 
import requests
import re
import os
#import logging

#import config variables
import config


#logging.getLogger("requests").propagate = False
#logging.getLogger("urllib3").propagate = False


#Function to convert datetime in UNIX epoch format to human readable datetime format
def convert_epoch_to_datetime(epoch_value):
	return(datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_value)), '%Y-%m-%d %H:%M:%S'))


#This function will search all the events within the time frame provided
#Returns the trigger_id and epoch datetime of the event
def get_events(date_start,date_end,request_id):
	# source value 0 means events type = 'trigger'
	e_source = "0"
	# object type 0 means events created by object 'trigger'
	e_object = "0"
	# value set to 1 means state of object is 'problem'
	e_value = "1"

	#build the api call data format
	payload = {"jsonrpc": "2.0","method": "event.get","params": {"source": e_source,"object": e_object,"value": e_value,"output": "extend","time_from": date_start,"time_till": date_end},"id": int(request_id),"auth": config.auth_code}
	
	#create the API call object
	connect = requests.post(config.api_url, data=json.dumps(payload), headers=config.headers, verify=False)
	#Clear screen
	os.system('cls')

	#Use the inbuilt json method of the api object to read the returned data
	for value in connect.json()['result']:
		#return data using python generator
		yield ((value.setdefault('objectid',''),value.setdefault('clock','')))


#This function takes in the trigger ids from the above function and returns the event description and hostid
def get_hostid(trigger_id,request_id):

	payload = {"jsonrpc": "2.0","method": "trigger.get","params": {"selectItems": "extend","output": "extend","triggerids": trigger_id},"id": int(request_id),"auth": config.auth_code}
	connect = requests.post(config.api_url, data=json.dumps(payload), headers=config.headers, verify=False)
	os.system('cls')

	raw_data = connect.json()

	return((raw_data['result'][0]['items'][0]['hostid'],raw_data['result'][0]['description']))


#This function takes in the hostid and returns the hostname
def get_hostname(host_id,request_id):

	payload = {"jsonrpc": "2.0","method": "host.get","params": {"hostids": host_id},"id": int(request_id),"auth": config.auth_code}
	connect = requests.post(config.api_url, data=json.dumps(payload), headers=config.headers, verify=False)
	os.system('cls')
	raw_data = connect.json()

	return(raw_data['result'][0]['name'])



#Main code
if __name__ == '__main__':

	request_id = 1

	csv_file = open(config.data_file, 'a')
	f_writer = csv.writer(csv_file)

	#Write the header ie the coloumn headings
	#f_writer.writerow(["Date & time", "HostName", "Alert Description"])

	#Create a regular expression object to replace the string {HOSTNAME} with actual hostnames in the alert description
	re_hostname = re.compile(r'{HOSTNAME}')
	    
	    
	print('Welcome to Zabbix Alerts Report generator\n')
	start_time = input('Enter the start date & time in Unix Epoch format: ')
	end_time = input('Enter the end date & time in Unix Epoch format: ')

	#Iterate for each event trigger id that is returned from the get_events function
	for trg_id,clock in get_events(start_time, end_time, request_id):

		#Get the hostid and alert description
	    request_id += request_id
	    hostid, desc = get_hostid(trg_id,request_id)

	    #Get the hostname from the hostid
	    request_id += request_id
	    hostname = get_hostname(hostid, request_id)

	    #Replace the strings {HOSTNAME} in the description with actual hostnames
	    desc = re_hostname.sub(hostname, desc)

	    os.system('cls')
	    prog = int((int(clock)-int(start_time))/(int(end_time)-int(start_time))*100)
	    print('Progress percentage : {} %'.format(prog))


	    #Convert epoch values to human readable date time
	    act_clock = convert_epoch_to_datetime(int(clock))

	    #Write values to file in csv format
	    f_writer.writerow([act_clock, str(hostname), str(desc)])

	del f_writer
	csv_file.close()
	os.system('cls')
	print('Progress percentage : 100 %')
	print('\nReport generated succefully')

	#32400
