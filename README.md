# Commerce API Documentation

https://apidocs-prod.cisco.com/ \
Upload RUM API: \
https://apidocs-prod.cisco.com/explore;category=6083723a25042e9035f6a753;epname=6083723b25042e9035f6a779;apiendpt=6419cdf54bef6e61d5f2b11b
Download API: \
https://apidocs-prod.cisco.com/explore;category=6083723a25042e9035f6a753;epname=6083723b25042e9035f6a779;apiendpt=6419cdf54bef6e61d5f2b116

# Notes
## Feature Documentation
- Documentation: Configure Smart Licensing Using Policy on Cisco IOS XE Routers \
Router not Connected to the CSSM and Without CSLU in Place \
https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-xe-17/217046-configure-smart-licensing-using-policy-o.html#toc-hId--721390126
~~~
Device(config)# license smart transport off
Device# license smart save usage all file bootflash:all_rum.txt 
Device# copy bootflash:all_rum.txt tftp://X.X.X.X/all_rum.txt
or...from Linux
scp -O admin@100.64.217.2://all_rum.txt all_rum.txt
~~~
Upload to CSSM.  Download Acknowledgement report.
~~~
Device# license smart import bootflash:ack_usage.txt 
~~~
## Script
- Script is incomplete at this time.  It currently will upload a RUM report and retrieve the response
- Use a Python venv
- Set the following environmental variables. A suggested way to do this is to use python venv
and add the following to the beginning of venv/bin/activate
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
