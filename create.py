import datetime

from CloudFlare.exceptions import CloudFlareAPIError
from requests import HTTPError

from main import account_id

def BlockListToMaxSize(block_list):
    res = []
    for i in range(0, len(block_list), 1000):
        res.append(block_list[i:i+1000])
    return res

def CreateValue(block_list):
    res = []
    for domain in block_list:
        res.append({"value": domain, "created_at": datetime.datetime.utcnow().isoformat() + "Z"})

    return res


def CreateLists(cf, block_list):
    split_block_list = BlockListToMaxSize(block_list)
    i = 1
    for block_list_split in split_block_list:
        name = "automated_adblock_{}".format(i)
        while True:
            try:
                cf.accounts.gateway.lists.post(account_id, data={"name": name, "type": "DOMAIN", "description": "automated_adblock", "items": CreateValue(block_list_split)})
            except HTTPError as e:
                print(e)
                continue
            except CloudFlareAPIError as e:
                print(e)
                break
            break

        print("Progress: {}/{}".format(i, len(split_block_list)))
        i += 1

def GetBlockListIds(cf):
    gateway_lists = cf.accounts.gateway.lists.get(account_id, params={'per_page': 150})

    res = []
    for gateway_list in gateway_lists:
        if gateway_list["type"] == "DOMAIN" and gateway_list["description"] == "automated_adblock":
            res.append(gateway_list["id"])

    return res

def CreateGatewayPolicies(cf):
    i = 0
    block_list_ids = GetBlockListIds(cf)
    for block_id in block_list_ids:
        i += 1
        name = "automated_adblock_{}".format(i)
        block_str = "any(dns.domains[*] in {})".format("$" + block_id)
        while True:
            try:
                cf.accounts.gateway.rules.post(account_id, data={"name": name, "action": "block", "enabled": True, "precedence": 1000 + i, "filters": ["dns"], "description": "automated_adblock", "traffic": block_str})
            except HTTPError as e:
                print(e)
                continue
            except CloudFlareAPIError as e:
                print(e)
                break
            break

        print("Progress {}/{}".format(i, len(block_list_ids)))

def CreateAll(cf, block_list):
    print("Creating new lists")
    CreateLists(cf, block_list)
    print("Created new lists")
    print("Creating new gateway policies")
    CreateGatewayPolicies(cf)
    print("Created new gateway policies")