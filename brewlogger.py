#pip install boto3
# add 
#  dtoverlay=w1-gpio,gpiopin=4
#  to /boot/config.txt and reboot
#  Setup your AWS s3 account permissions as per:
#  https://realpython.com/python-boto3-aws-s3/  check for instructions under the Installation header


import os
import glob
import time
from datetime import datetime

import csv
import boto3

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
log_dir = '/tmp/'
loopcount = 0
uploadfreq = 6
sleep_interval = 1
log_filename = 'brewlog.txt'
log_fileloc = log_dir+log_filename
log_header = 'TimeReading,TEMP1C,TEMP1F\r\n'

logdateformat = "%Y/%m/%d %H:%M:%S"



def upload_file():
    print('file uploading')
    s3 = boto3.resource('s3')
    BUCKET = 'bungobrew.co.uk'
    s3.Bucket(BUCKET).upload_file(log_fileloc, "brewlogging/"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.csv')

def reset_log():
    with open(log_fileloc, mode='w') as new_log:
        new_log.write(log_header)
        new_log.close()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


reset_log()
while True:
    loopcount = loopcount + 1
    temp_c = read_temp()
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    with open(log_fileloc, mode='a') as brew_logfile:
        brewlog_writer = csv.writer(brew_logfile, delimiter=',', quotechar='"',  quoting=csv.QUOTE_MINIMAL)
        brewlog_writer.writerow([datetime.now().strftime(logdateformat),temp_c, temp_f])        
    brew_logfile.close()
    if loopcount == uploadfreq:
        loopcount = 0 #reset the counter
        #connect to s3 and upload
        print("uploading the file to S3")
        upload_file()
        print("deleting the log file")
        reset_log()
    time.sleep(sleep_interval)
