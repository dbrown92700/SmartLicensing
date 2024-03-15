# Overview
This script automates offline licensing for routers using Smart Licensing Using Policy using the Cisco Commerce API
## Feature Documentation
- Documentation: Configure Smart Licensing Using Policy on Cisco IOS XE Routers \
Router not Connected to the CSSM and Without CSLU in Place \
https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-xe-17/217046-configure-smart-licensing-using-policy-o.html#toc-hId--721390126

## Manual (Non-automated) Steps
Configure Device and generate RUM report:
~~~
Device(config)# license smart transport off
Device# license smart save usage all file bootflash:all_rum.txt 
Device# copy bootflash:all_rum.txt tftp://X.X.X.X/all_rum.txt

or...from Linux

scp -O admin@10.1.2.3://all_rum.txt all_rum.txt
~~~
Upload to CSSM.  Download Acknowledgement report. Upload to device. Apply ack to device:
~~~
scp -O ack_usage.txt admin@10.1.2.3://ack_usage.txt
Device# license smart import bootflash:ack_usage.txt 
~~~

# Commerce API Documentation

https://apidocs-prod.cisco.com/ \
Upload RUM API: \
https://apidocs-prod.cisco.com/explore;category=6083723a25042e9035f6a753;epname=6083723b25042e9035f6a779;apiendpt=6419cdf54bef6e61d5f2b11b
Download API: \
https://apidocs-prod.cisco.com/explore;category=6083723a25042e9035f6a753;epname=6083723b25042e9035f6a779;apiendpt=6419cdf54bef6e61d5f2b116


## Script Setup
- Clone Repository
> git clone https://github.com/dbrown92700/SmartLicensing
- Use a Python venv. In the SmartLicensing directory 
> python -m venv venv
- Install python requirements
> pip install -r requirements.txt
- Create an app account on the Commerce API website.  Under the Console tab, "Create API Client".  App Type: Native.  Redirect URL: anything.
Associate APIs: add all.  You can restrict API's, but I haven't tested that.
- Set the following environmental variables. A suggested way to do this is to use python venv
and add the following to the beginning of venv/bin/activate
- CLINT_ID & CLIENT_SECRET are from the API Client.
- SMART_ACCOUNT and VIRTUAL_ACCOUNT numeric ID's can be found in the url by browsing to software.cisco.com ->
Manage Smart Account -> Virtual Accounts. 
For example (https://software.cisco.com/software/csws/smartaccount/virtualAccounts/123456/editVA/456789)
~~~
# ENVIRONMENT VARIABLES ADDITIONS FOR SMART LICENSE SCRIPT
export CLIENT_ID='1111111-2222222-333333333'
export CLIENT_SECRET='11111111-2222222-3333333'
export CCO_USERNAME='your_username'
export CCO_PASSWORD='your_password'
export SA_DOMAIN='your-smart-account-domain.com'
export SMART_ACCOUNT='123456'
export VIRTUAL_ACCOUNT='456789'
~~~
# Usage
If you supply a router ID and credentials, the script will log into the router, generate a RUM report, SCP to a local
file, upload to CSSM, get the response, SCP the response to the router, and apply the acknowledgement.

> ./main.py -a 10.1.2.3 -u admin -p password

Alternatively, you can handle the router upload/download manually by omitting the arguments. Make sure the RUM report 
is saved in the local directory as rum_all.txt before executing.

> ./main.py

Validate that the acknowledgement worked:
~~~
router#show license all | i Last ACK
  Last ACK received: Mar 15 21:18:58 2024 UTC
~~~
# Author

David Brown, davibrow@cisco.com
