#!python
from smart_license import SmartLicensePortal
from rum_report import RumReport
import os
import json

# Set environment variables prior to executing
# See readme.md for details

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
cco_username = os.getenv('CCO_USERNAME')
cco_password = os.getenv('CCO_PASSWORD')
sa_domain = os.getenv('SA_DOMAIN')
smart_account = os.getenv('SMART_ACCOUNT')
virtual_account = os.getenv('VIRTUAL_ACCOUNT')

if __name__ == '__main__':

    portal = SmartLicensePortal(client_id=client_id, client_secret=client_secret, cco_username=cco_username,
                                cco_password=cco_password, sa_domain=sa_domain)

    # Sample call to retrieve accounts.  This will help ensure that the user has access to the Smart Account
    # accounts = portal.api_call(portal.Urls.accounts['method'], portal.Urls.accounts['url'])
    # print(accounts.json())

    # Import a device RUM file
    report = RumReport()
    report.read_file('all_rum.txt')
    print(f'RUM:\n{report.rum_json}')

    device_info = json.loads((report.rum_json['smartLicense']['smartLicenseSystemInfo']['data']))

    headers = report.virtual_account_header(smart_account=smart_account, virtual_account=virtual_account)

                                            # udi_pid=device_info['sudi']['udi_pid'],
                                            # udi_sn=device_info['sudi']['udi_serial_number'],
                                            # hostname=device_info['hostname'])

    # Upload RUM file to CSSM
    report.create_rum_payload()
    print(f'\nPayload:\n\n{report.upload_payload}')

    response = portal.api_call(portal.Urls.reportUsage['method'], portal.Urls.reportUsage['url'],
                               payload=report.upload_payload, headers=headers)

    print(f'RESPONSE:\n{response}:{response.text}')
    poll_id = response['poll_id']
    timestamp = response['timestamp']
    print(f'POLL ID: {poll_id}')

    # Retrieve RUM Authorization
    report.create_poll_payload(poll_id, timestamp)
    response = portal.api_call(portal.Urls.poll['method'], portal.Urls.poll['url'], payload=report.poll_payload,
                               headers=headers)
    print(f'AUTH:\n{response}')


