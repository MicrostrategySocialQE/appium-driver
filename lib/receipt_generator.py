import time
import logging

from lib import receipts_data
from lib.alert_api_caller import APICaller
from suite import configs


log = logging.getLogger("__main__")


def receipts_formatter(auid, shopid=None):
    data = receipts_data.receipt_data
    tt = str(int(time.time()))
    for item in data:
        if isinstance(item, dict):
            item = [item]
        for subitem in item:
            subitem['auid'] = auid
            if shopid and 'shop_id' in subitem:
                subitem['shop_id'] = shopid
            subitem['transaction_id'] += str(tt)
    return data


def delete_receipts_data(config):
    """
    delete all receipts from user's wallet

    config: (dictionary parameter)
        environment:
        application:
        account:
            email:
            password:
    """
    apicaller = APICaller(config["environment"], config["application"])
    account = config["account"]
    account_info = apicaller.user_me_start2(account['email'], account['password'])

    token = account_info["token"]
    receipts = apicaller.user_me_receipts(token)
    for receipt in receipts:
        receipt_detail = apicaller.receipt_detail(receipt['order_id'], token)
        if not apicaller.delete_receipt(receipt_detail['transaction_id']):
            print "deleting receipt failed."


def populate_receipts(config):
    """
    delete all receipts from user's wallet

    config: (dictionary parameter)
        environment:
        application:
        account:
            email:
            password:
    """
    apicaller = APICaller(config["environment"], config["application"])
    account = config["account"]
    account_info = apicaller.user_me_start2(account['email'], account['password'])

    receipts = receipts_formatter(account_info['uvs_id'], shopid=config['shop_id'])
    for receipt in receipts:
        if not apicaller.create_receipt(receipt):
            print "creating receipt failure."


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s %(message)s")
    ch.setFormatter(formatter)
    log.addHandler(ch)

    config = configs.config
    populate_receipts(config)