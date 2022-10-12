from requests import HTTPError
from CloudFlare.exceptions import CloudFlareAPIError

from main import account_id

def GetGatewayPoliciesToDelete(cf):
    gateway_policies = cf.accounts.gateway.rules.get(account_id)

    to_delete = []
    for gateway_policy in gateway_policies:
        if gateway_policy["description"] == "automated_adblock":
            to_delete.append(gateway_policy["id"])

    return to_delete

def DeleteOldGatewayPolicies(cf):
    for to_delete in GetGatewayPoliciesToDelete(cf):
        while True:
            try:
                cf.accounts.gateway.rules.delete(account_id, to_delete)
            except HTTPError as e:
                print(e)
                continue
            except CloudFlareAPIError as e:
                print(e)
                break
            break

def GetListsToDelete(cf):
    gateway_lists = cf.accounts.gateway.lists.get(account_id)

    to_delete = []
    for gateway_list in gateway_lists:
        if gateway_list["type"] == "DOMAIN" and gateway_list["description"] == "automated_adblock":
            to_delete.append(gateway_list["id"])

    return to_delete

def DeleteOldLists(cf):
    for to_delete in GetListsToDelete(cf):
        while True:
            try:
                cf.accounts.gateway.lists.delete(account_id, to_delete)
            except HTTPError as e:
                print(e)
                continue
            except CloudFlareAPIError as e:
                print(e)
                break
            break

def DeleteAll(cf):
    print("Deleting old gateway policies")
    DeleteOldGatewayPolicies(cf)
    print("Deleted old gateway policies")
    print("Deleting old lists")
    DeleteOldLists(cf)
    print("Deleted old lists")