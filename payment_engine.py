import pandas as pd
import sys
from client import Client


def read_csv(file_name):
    data = pd.read_csv(file_name)
    return data


def do_deposit(client, value):
    client.modify_available(value)
    client.modify_total(value)


def do_withdrawal(client, value):
    if client.get_available() >= value:
        client.modify_available(-1 * value)
        client.modify_total(-1 * value)


def do_dispute(client, value):
    client.modify_held(value)
    client.modify_available(-1 * value)


def do_resolve(client, value):
    client.modify_held(-1 * value)
    client.modify_available(value)


def do_chargeback(client, value):
    client.modify_held(-1 * value)
    client.modify_total(-1 * value)
    client.lock_client()


def main(filename):
    input_file = str(filename)
    data = read_csv(filename)

    # Sanitize data
    # Negative values should not come from the csv
    list_of_amounts = data['amount'].values
    if len(list(filter(lambda x: (x < 0), list_of_amounts))) > 0:
        raise Exception("Negative value in the csv, suspicious csv file " + input_file + " aborting")

    # withdrawals should not be disputed, resolved nor chargeback should happen on it
    withdrawals_tx = set(data.loc[data['type'] == 'withdrawal']['tx'].values)
    disp_resol_charge_tx = set(data.loc[data['type'].isin(['dispute', "resolve", "chargeback"])].tx.values)
    intersection = withdrawals_tx.intersection(disp_resol_charge_tx)
    if len(intersection) > 0:
        raise Exception("Withdrawals cannot be changed")

    # csv looks good
    # select uniq clients and create clients
    unique_clients = set(data['client'].values)
    client_list = []
    for client in unique_clients:
        client_list.append(Client(client))

    # create transactions
    transactions_dict = {}
    deposit_and_withdrawal_data = data.loc[data["type"].isin(["deposit", "withdrawal"])]

    # create dict from deposit/withdraw transactions
    for index, row in deposit_and_withdrawal_data.iterrows():
        transactions_dict.update({row['tx']: row['amount']})

    for index, row in data.iterrows():
        for client in client_list:
            if client.get_client_id() == row['client']:

                if row['type'] == 'deposit':
                    do_deposit(client, row['amount'])

                if row['type'] == 'withdrawal':
                    do_withdrawal(client, row['amount'])

                if row['type'] == 'dispute':
                    try:
                        dispute_value = transactions_dict[row['tx']]
                        do_dispute(client, dispute_value)
                    except KeyError:
                        # client side error
                        pass

                if row['type'] == 'resolve':
                    try:
                        resolve_value = transactions_dict[row['tx']]
                        do_resolve(client, resolve_value)
                    except KeyError:
                        # client side error
                        pass

                if row['type'] == 'chargeback':
                    try:
                        chargeback_value = transactions_dict[row['tx']]
                        do_chargeback(client, chargeback_value)
                    except KeyError:
                        # client side error
                        pass

    print("client, available, held, total, locked")
    for client in client_list:
        client_id, available, held, total, locked = client.get_client_data()
        print("{}, {}, {}, {}, {}".format(client_id, available, held, total, locked))


if __name__ == "__main__":
    main(sys.argv[1])
