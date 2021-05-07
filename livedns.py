import sys
import requests
import json
from dotenv import dotenv_values


# get the current public IP address
def get_ip():
    ip = requests.get("https://icanhazip.com")
    return ip.text.rstrip()


# get the current IP within the A record
def get_record(record, domain, headers):
    dom = requests.get(f'https://api.gandi.net/v5/livedns/domains/{domain}/records/{record}', headers=headers)
    liveRecord = json.loads(dom.text)[0]

    return liveRecord["rrset_values"][0]


# set the A record with the public IP, as well as the TTL from .env
def set_record(record, domain, ttl, ip, headers):
    data = {
        "items": [ {
            "rrset_type": "A",
            "rrset_values": [f'{ip}'],
            "rrset_ttl": f'{int(ttl)}'
        }]
    }
    update = requests.put(f'https://api.gandi.net/v5/livedns/domains/{domain}/records/{record}', headers=headers, json=data)
    print(data)


def main():
    # read the config from the .env file (but don't push them as env vars)
    config = dotenv_values(".env")
    if not config:
        print("Please create .env or rename .env.example to .env")
        sys.exit(1)
    # common header to share with funcs
    headers = {
        "Authorization": f'Apikey {config["gandi_api_key"]}'
    }
    # get the current public ip
    ip = get_ip()
    # get the current A record
    record = get_record(
        config["record"],
        config["domain"],
        headers)

    # check if the current public ip and the A record match
    if record != ip:
        # if not, update the record
        set_record(
            config["record"],
            config["domain"],
            config["ttl"],
            ip,
            headers)
    else:
        print(f'Record {record} and Public IP {ip} currently match...')


if __name__ == '__main__':
    # do the things
    main()
