import json
import xmltodict
from time import time


class RumReport:

    def __init__(self):
        self.rum_json = {}
        self.upload_payload = {}
        self.poll_payload = {}

    def read_file(self, filename='all_rum.txt'):

        # Parses all_rum file from device to rum_json

        with open(filename) as file:
            rum_xml = file.read()
            self.rum_json = xmltodict.parse(rum_xml)

    @staticmethod
    def virtual_account_header(smart_account: str, virtual_account: str, udi_pid: str, udi_sn: str, hostname: str):
        req_sys = json.dumps({"udi_pid": udi_pid,
                              "udi_serial_number": udi_sn,
                              "display_name": hostname,
                              "host_identifier": hostname})
        headers = {
            'Accept': '*/*',
            'Content-type': 'application/json',
            'X-CSW-REQUESTING-SYSTEM': req_sys,
            'X-CSW-SMART-ACCOUNT-ID': smart_account,
            'X-CSW-VIRTUAL-ACCOUNT-ID': virtual_account
        }
        # headers = {
        #     'Accept': '*/*',
        #     'Content-type': 'application/json',
        #     'X-CSW-REQUESTING-SYSTEM': 'PYTHON_SCRIPT',
        #     'X-CSW-SMART-ACCOUNT-ID': smart_account,
        #     'X-CSW-VIRTUAL-ACCOUNT-ID': virtual_account
        # }

        return headers

    def create_rum_payload(self):

        # Creates CSSM request payload from rum_json

        usages = []
        for usage in self.rum_json['smartLicense']['RUMReport']:
            jusage = json.loads(usage)
            usages.append(
                {
                    "payload": jusage['payload'],
                    "signature": jusage['signature'],
                    "is_consuming": None,
                    "is_ha": None,
                    "reporting_device": None,
                    "errors": None
                }
            )

        sys = json.loads(self.rum_json['smartLicense']['smartLicenseSystemInfo']['data'])

        self.upload_payload = {
            "data": {
                'sudi': sys['sudi'],
                "timestamp": sys['timestamp'],
                "nonce": sys['nonce'],
                'product_instance_identifier': None,
                "reports": [
                    {
                        "sudi": sys['sudi'],
                        'hostname': sys['hostname'],
                        'software_tag_identifier': sys['software_tag_identifier'],
                        "nonce": sys['nonce'],
                        "timestamp": sys['timestamp'],
                        "trust_requests": None,
                        "transaction_id": None,
                        "requesting_user_id": None,
                        "locale": None,
                        "license_pool_id": None,
                        "product_instance_controller_id": None,
                        'usage': usages
                    }
                ]
            },
            "requesting_user_id": None,
            "locale": None
        }

    def create_poll_payload(self, rum_response: dict):

        self.poll_payload = {
            "data": {
                "timestamp": rum_response['timestamp'],
                "nonce": rum_response['nonce'],
                "poll_id": rum_response['poll_id'],
                "type": "authorizations",
                "action": "acknowledgements"
            }
        }