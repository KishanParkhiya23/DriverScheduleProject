import csv
import re 
from DriverSchedule_app.models import *
from django.contrib.auth.models import User


def dateConvert(date_):
    date_ = date_.split('/')
    year_ ='20' + date_[-1]
    return year_ + '-' + date_[1] + '-' + date_[0]

mobile_pattern = '[0-9]{10}'
def get_valid_mobile_number(mobile_no):
    while True:        
        if re.fullmatch(mobile_pattern, mobile_no):
            return mobile_no
        else:
            return None
            
def insertIntoModel(dataList):
    while dataList:
        dump = dataList[:4]
        mobile_no = dump[1].strip()
        M_pattern = get_valid_mobile_number(mobile_no)
        users = User.objects.all()

# Create lists to store usernames and email addresses
        usernames = [user.username for user in users]
        email_addresses = [user.email for user in users]
        if dump[1].strip() == M_pattern and dump[0].strip().replace(' ','') not in usernames and dump[2].strip().replace(' ','') not in email_addresses:
            DriverObj = Driver()
            # truckCostObj.docketNo = DocketPDF.objects.filter(docketNumber = DocketPDFobj.docketNumber).first()
            DriverObj.name = dump[0].strip().replace(' ','')
            DriverObj.phone = dump[1].strip() 
            DriverObj.email = dump[2].strip().replace(' ','')
            DriverObj.password = dump[3].strip()
            DriverObj.save()
            user_ = User.objects.create(username=DriverObj.name, email=DriverObj.email, password=DriverObj.password, is_staff=True)
            user_.set_password(DriverObj.password)
            user_.save()
        break
            # user_.set_password(password1)

        
f = open("Driver_reg_file.txt",'r')
file_name = f.read()

files = open(f'static/img/driverRegFile/{file_name}','r')
reader=csv.reader(files)
next(reader)
for row in reader:
    insertIntoModel(row)