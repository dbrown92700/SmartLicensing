import json
import xmltodict


class SlacReport:

    def __init__(self):
        self.slac_req_json = {}
        self.upload_payload = {}
        self.poll_payload = {}
        self.sys_info = {}
        self.auth_reqeust = {}

    def read_file(self, filename='slac.txt'):

        # Parses all_rum file from device to rum_json

        with open(filename) as file:
            slac_xml = file.read()
            self.slac_req_json = xmltodict.parse(slac_xml)

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

        return headers

    def create_slac_req_payload(self):

        self.sys_info = json.loads(self.slac_req_json['smartLicense']['smartLicenseSystemInfo']['data'])
        self.auth_reqeust = json.loads(self.slac_req_json['smartLicense']['smartLicenseAuthRequest']['data'])

        self.upload_payload = {
            "data": {
                "timestamp": self.sys_info['timestamp'],
                "nonce": self.sys_info['nonce'],
                "licenses": [
                    {
                        "sudi": self.auth_reqeust[0]['sudi'],
                        "software_tag_identifier": self.sys_info['device_list'][0]['software_tag_identifier'],
                        "hostname": self.sys_info['device_list'][0]['hostname'],
                        "trust_request": self.sys_info['device_list'][0]['hostname'],
                        "keys": self.auth_reqeust[0]['keys'],
                        "confirm_code": self.auth_reqeust[0]['confirm_code'],
                        "remove_code": self.auth_reqeust[0]['remove_code']
                    }
                ]
            }
        }

    def create_poll_payload(self, slac_response: dict):

        self.poll_payload = {
            "data": {
                "timestamp": slac_response['timestamp'],
                "nonce": slac_response['nonce'],
                "poll_id": slac_response['poll_id'],
                "type": "authorizations",
                "action": "authorizations"
            }
        }