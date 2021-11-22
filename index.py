import sys
import re
import os
import requests
import json
import uuid
from netaddr import IPNetwork

pattern = re.compile("[a-z0-9-]+")


if len(sys.argv) != 2:
    print("you have to pass one argument and that is region")
    print("you can execute the program with the folowing command")
    print("python index.py <region>")
    sys.exit()

if not pattern.fullmatch(sys.argv[1]):
    sys.exit("provided region can only contain only this caharacter \n a-z,0-9,- ")

os.mkdir("incoming")
os.mkdir("ec2_by_region")
os.mkdir("ec2_filtered")

url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
r = requests.get(url, allow_redirects=True)


open('incoming/ip-ranges.json', 'wb').write(r.content)
f = open('incoming/ip-ranges.json',)
data = json.load(f)
f.close()
 
for i in data['prefixes']:
    if i['service'] == 'EC2':
        i['id'] = str(uuid.uuid4())
        open('ec2_by_region/{0}{1}'.format(i['region'],".json"),'a').write(json.dumps(i)+"\n")

        if i['region'] == sys.argv[1]:
            open('ec2_filtered/{0}{1}'.format(i['id'],".json"),'a').write(json.dumps(i)+"\n")
