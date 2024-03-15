#!python
import time

from smart_license import SmartLicensePortal
from rum_report import RumReport
import os
import json
from router import Router
import argparse
import base64

# Set environment variables prior to executing
# See readme.md for details

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
cco_username = os.getenv('CCO_USERNAME')
cco_password = os.getenv('CCO_PASSWORD')
sa_domain = os.getenv('SA_DOMAIN')
smart_account = os.getenv('SMART_ACCOUNT')
virtual_account = os.getenv('VIRTUAL_ACCOUNT')


def get_rum(router_ip: Router, local_file='all_rum.txt'):

    cmd_result = router_ip.send_command('license smart save usage all file bootflash:all_rum.txt')
    if cmd_result != '':
        return 'Failed to issue save usage command'
    try:
        router_ip.get_file(local_file, 'all_rum.txt')
    except Exception as e:
        return f'Failed: {e}'

    return 'Success'


def send_ack(router_ip: Router, local_file='ack_usage.txt'):

    router_ip.send_file(local_file=local_file, remote_file='ack_usage.txt')
    try:
        cmd_result = router_ip.send_command('license smart import bootflash:ack_usage.txt', 'Import Data Successful')
    except Exception as e:
        return f'Failed: {e}'

    return 'Success'


if __name__ == '__main__':

    cli_help = 'Uploads RUM reports and downloads the response. Will connect to router to complete this if' \
           'it is specified in the arguements. If not, place the all_rum.txt file in this directory' \
           'before executing.'
    cli_parser = argparse.ArgumentParser(description=cli_help)
    cli_parser.add_argument('-a', '--address', metavar='<router-ip>', required=False,
                            help='Specify router IP to download RUM and upload ACK. If router is not specified'
                                 'script will look for an existing all_rum.txt file in this directory.')
    cli_parser.add_argument('-u', '--user', metavar='<user>', required=False,
                            help='Username is required if router is specified')
    cli_parser.add_argument('-p', '--password', metavar='<password>', required=False,
                            help='Password is requried if router is specified.')

    cli_args = cli_parser.parse_args()

    if cli_args.address:
        router = Router(cli_args.address, cli_args.user, cli_args.password)
        print(f'Router status: {router.status}')
        result = get_rum(router_ip=router, local_file='all_rum.txt')
        print(f'RUM Download: {result}')

    portal = SmartLicensePortal(client_id=client_id, client_secret=client_secret, cco_username=cco_username,
                                cco_password=cco_password, sa_domain=sa_domain)

    # Sample call to retrieve accounts.  This will help ensure that the user has access to the Smart Account
    # accounts = portal.api_call(portal.Urls.accounts['method'], portal.Urls.accounts['url'])
    # print(accounts.json())

    # Import a device RUM file
    report = RumReport()
    report.read_file('all_rum.txt')

    device_info = json.loads((report.rum_json['smartLicense']['smartLicenseSystemInfo']['data']))

    headers = report.virtual_account_header(smart_account=smart_account, virtual_account=virtual_account,
                                            udi_pid=device_info['sudi']['udi_pid'],
                                            udi_sn=device_info['sudi']['udi_serial_number'],
                                            hostname=device_info['hostname'])

    # Upload RUM file to CSSM
    report.create_rum_payload()
    print(f'\nRUM Payload:\n\n{report.upload_payload}')

    response = portal.api_call(portal.Urls.reportUsage['method'], portal.Urls.reportUsage['url'],
                               payload=report.upload_payload, headers=headers)

    print(f'RESPONSE:\n{response}:{response.text}')

    # Retrieve RUM Authorization and save to file
    report.create_poll_payload(json.loads(response.text))
    while True:
        # Poll for complete status
        response = portal.api_call(portal.Urls.poll['method'], portal.Urls.poll['url'], payload=report.poll_payload,
                                   headers=headers)
        print(f'AUTH:\n{response}:{response.text}')
        j_response = json.loads(response.text)
        if j_response['status'] == 'COMPLETE':
            break
        time.sleep(10)
    ack = base64.b64decode(j_response['data']['acknowledgements'][0]['smart_license']).decode()
    with open('ack_usage.txt', 'w') as file:
        file.write(ack)

    # Upload ACK to router
    if cli_args.address:
        result = send_ack(router, 'ack_usage.txt')
        print(f'Acknowledge apply: {result}')
        router.disconnect()
