from web3 import Web3


def main():
    w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/df118709d9c04cf6aee4d6f7bd943f80"))
    print(w3.isConnected())
    print(w3.eth.get_block("latest"))


if __name__ == '__main__':
    main()