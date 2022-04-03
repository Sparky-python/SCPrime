#!/usr/bin/env python3

import subprocess as sp
import os
import requests
import json

def check_open_ports(ip):

  url = "https://api.geekflare.com/openport"

  payload = json.dumps({
    "url": "https://" + ip
  })
  headers = {
    'x-api-key': '5e3dc3ec-c890-406c-9120-740fa34829bd',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  port_list = json.loads(response.text)['data']
  return(port_list)

def are_spd_ports_open(spd_port, open_ports_list):

  spd_port_num = int(spd_port)
  spd_port_num2 = spd_port_num + 1
  spd_port_num3 = spd_port_num + 3

  if spd_port_num in open_ports_list:
    print ("Port " + str(spd_port_num) + " is correctly forwarded")
  else:
    print ("Port " + str(spd_port_num) + " is not forwarded correctly or is blocked by a firewall")

  if spd_port_num2 in open_ports_list:
    print ("Port " + str(spd_port_num2) + " is correctly forwarded")
  else:
    print ("Port " + str(spd_port_num2) + " is not forwarded correctly or is blocked by a firewall")

  if spd_port_num3 in open_ports_list:
    print ("Port " + str(spd_port_num3) + " is correctly forwarded")
  else:
    print ("Port " + str(spd_port_num3) + " is not forwarded correctly or is blocked by a firewall")




spd_path = sp.getoutput("find / -name spd -type f 2>/dev/null")
spc_path = sp.getoutput("find / -name spc -type f 2>/dev/null")
metadata_path = sp.getoutput("find / -name consensus -type d 2>/dev/null")
spd_user = sp.getoutput("ps -ef | grep spd")
spc_host_v = sp.getoutput(spc_path + " host -v")
spc = sp.getoutput(spc_path)
public_ip = sp.getoutput("dig +short myip.opendns.com @resolver1.opendns.com")

storage = False
storage_folders = []

lines = spc_host_v.splitlines()
for line in lines:
  if "Connectability Status" in line:
    connectability_status = line.split(":")[1].strip()
  elif "Provider ID" in line:
    provider_ID = line.split(":")[1].strip()
  elif "Version" in line:
    version = line.split(":")[1].strip()
  elif "netaddress" in line:
    netaddress = line.split(":")[1].strip()
    announced_port = line.split(":")[2].strip().split(" ")[0]
  elif "collateral" in line:
    collateral = line.split(":")[1].strip()
  elif "Storage Folders" in line:
    storage = True
  elif storage == True:
    storage_folders.append(line)



wallet = False
lines = spc.splitlines()
for line in lines:
  if "Synced" in line:
    synced = line.split(":")[1].strip()
  elif "Wallet" in line:
    wallet = True
  elif ("Status" in line) and wallet:
    status = line.split(":")[1].strip()
    wallet = False

port_list = check_open_ports(public_ip)

print ("#######################")#
print ("Your public IP address is: " + public_ip)
print ("SPD is running on port " + announced_port)

are_spd_ports_open(announced_port, port_list)
if "Host appears to be working" in connectability_status:
  print ("SPD is working fine")
elif "connectable" in connectability_status:
  print ("SPD not working, check port forwarding")
else:
  print ("SPD has a problem")

print("Your open ports are as follows:")
for port in port_list:
  print(port)


