# Overview
This script automates offline licensing for routers using Smart Licensing Using Policy using the Cisco Commerce API.
If you supply router credentials, the script will log into the router to generate both a SLAC request and RUM report, upload both to CSSM,
retrieve the responses and apply it to the router.

Note that for hardware routers, the SLAC process must be completed before the throughput can be set above 250 Mbps, so you must complete
the SLAC workflow before you can set DNA Advantage Tier 2 or above license.  After you have completed these steps you can complete
the RUM workflow.  See "Before you begin" in Configuring a Tier-Based Throughput: https://www.cisco.com/c/en/us/td/docs/routers/cloud_edge/c8300/software_config/cat8300swcfg-xe-17-book/m-available-licenses.html#configuring-a-tier-based-throughput

# Reference Information
### Feature Documentation
Documentation: Configure Smart Licensing Using Policy on Cisco IOS XE Routers\

Installing SLAC for HSECK9 on a router:
https://www.cisco.com/c/en/us/td/docs/routers/cloud_edge/c8300/software_config/cat8300swcfg-xe-17-book/m-available-licenses.html#Cisco_Concept.dita_ea5e5a1c-0f4a-4ef9-8633-f83310a359a5 \
Router not Connected to the CSSM and Without CSLU in Place: https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-xe-17/217046-configure-smart-licensing-using-policy-o.html#toc-hId--721390126

Task Library for Smart Licensing Using Policy: 
- SLAC:
  1. Generating and Saving a SLAC Request on the Product Instance: https://www.cisco.com/c/en/us/td/docs/routers/sl_using_policy/b-sl-using-policy/task_library.html#Cisco_Task.dita_74ea21ec-53d5-4af8-a698-805416101e37
  2. Manually Requesting and Auto-Installing a SLAC: https://www.cisco.com/c/en/us/td/docs/routers/sl_using_policy/b-sl-using-policy/task_library.html#Cisco_Task.dita_f42f2f6d-2f5c-4115-bd20-fbf6e190a199
  3. Installing a File on the Product Instance: https://www.cisco.com/c/en/us/td/docs/routers/sl_using_policy/b-sl-using-policy/task_library.html#Cisco_Task.dita_f42f2f6d-2f5c-4115-bd20-fbf6e190a199
- RUM:
  1. Workflow for Topology: No Connectivity to CSSM and No CSLU: https://www.cisco.com/c/en/us/td/docs/routers/sl_using_policy/b-sl-using-policy/how_to_configure_workflows.html#Cisco_Concept.dita_7057e18c-3c69-4d91-841b-0b5beb7a2d8
  2. Installing a File on the Product Instance: https://www.cisco.com/c/en/us/td/docs/routers/sl_using_policy/b-sl-using-policy/task_library.html#Cisco_Task.dita_f42f2f6d-2f5c-4115-bd20-fbf6e190a199

### Manual (Non-automated) Steps
For reference, these are the manual steps that the script is emulating.

1. Configure Device and generate RUM report:
~~~
Device(config)# license smart transport off
Device# license smart save usage all file bootflash:all_rum.txt 
Device# copy bootflash:all_rum.txt tftp://X.X.X.X/all_rum.txt

or...from Linux

scp -O admin@10.1.2.3://all_rum.txt all_rum.txt
~~~
2. Upload to CSSM.
3. Download Acknowledgement report.
4. Upload ack to device.
5. Apply ack to device:
~~~
scp -O ack_usage.txt admin@10.1.2.3://ack_usage.txt
Device# license smart import bootflash:ack_usage.txt 
~~~

### Commerce API Documentation

https://apidocs-prod.cisco.com/

Upload RUM API: \
https://apidocs-prod.cisco.com/explore;category=6083723a25042e9035f6a753;epname=6083723b25042e9035f6a779;apiendpt=6419cdf54bef6e61d5f2b11b

Download API: \
https://apidocs-prod.cisco.com/explore;category=6083723a25042e9035f6a753;epname=6083723b25042e9035f6a779;apiendpt=6419cdf54bef6e61d5f2b116


# Script Setup
- Clone Repository
> git clone https://github.com/dbrown92700/SmartLicensing
- Use a Python venv. In the SmartLicensing directory 
> python -m venv venv \
> source venv/bin/activate
- Install python requirements
> pip install -r requirements.txt
- Request access to the commerce API:
  - From: https://apidocs-prod.cisco.com/explore
  - Navigate to "Smart Accounts & Licensing API"
  - Navigate to "Smart Licensing Using Policy"
  - "Access Request"
  - Repeat for "Smart Accounts" (not strictly needed, but this is included in the code for simple testing purposes)
  - Proceed to the next step once access is granted
- Create an app account on the Commerce API website.
  - Under the Console tab, "Create API Client".
  - App Type: Native.
  - Redirect URL: anything.
  - Associate APIs: add all.  You can restrict API's, but I haven't tested that.


- Set the following environmental variables.
  - A suggested way to do this is to use python venv
  and add the following to the beginning of venv/bin/activate
  - CLINT_ID & CLIENT_SECRET are from the Commerce API Client.
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

> ./main.py --slac --rum -a 10.1.2.3 -u admin -p password

The --slac and --rum arguments are used to run the SLAC and RUM workflows respectively. Omitting one will skip that workflow. 

Alternatively, you can handle the router upload/download manually by omitting the arguments. Make sure the SLAC and/or RUM
reports are saved in the local directory as slac.txt and rum_all.txt before executing.

> ./main.py --rum \
> ./main.py --slac

Validate that the acknowledgement worked:
~~~
router#show license all | i Last ACK
  Last ACK received: Mar 15 21:18:58 2024 UTC
~~~
# Author

David Brown, davibrow@cisco.com
