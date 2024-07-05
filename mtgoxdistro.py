import requests
import time


def get_address_details(address):
    """Retrieve detailed information about the specified Bitcoin address."""
    url = f"https://blockchain.info/rawaddr/{address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for address {address}: HTTP {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


def main():
    # The initial address to check (e.g., Mt. Gox distribution address)
    mtgox_address = "1JbezDVd9VsK9o1Ga9UqLydeuEvhKLAPs6"
    mtgox_details = get_address_details(mtgox_address)

    if mtgox_details is None:
        return

    # Analyze the outputs of all transactions to find addresses that received more than 10 BTC
    address_amounts = {}
    for tx in mtgox_details.get('txs', []):
        for output in tx.get('out', []):
            if 'addr' in output and output['value'] > 0:
                addr = output['addr']
                amount = output['value'] / 1e8  # Convert satoshis to BTC
                if addr in address_amounts:
                    address_amounts[addr] += amount
                else:
                    address_amounts[addr] = amount

    # Filter addresses that have received more than 10 BTC
    important_addresses = {addr: amt for addr, amt in address_amounts.items() if amt > 10}

    # Display balances for these addresses
    for addr, total_received in important_addresses.items():
        print(f"\nAddress {addr} received a total of {total_received:.8f} BTC.")
        time.sleep(10)  # Delay to prevent hitting the API rate limit
        details = get_address_details(addr)
        if details:
            current_balance = details.get('final_balance', 0) / 1e8
            print(f"  Current balance: {current_balance:.8f} BTC")


if __name__ == "__main__":
    main()
