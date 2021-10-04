from scripts.utils import get_account, encode_function_data, upgrade
from brownie import network, Contract, Box, BoxV2, BoxAdmin, BoxProxy


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}...")

    box = Box.deploy({"from": account})
    print(box.retrieve())  # should return 0

    box_admin = BoxAdmin.deploy({"from": account})

    # example initializer (init method to be called and optional arguments):
    #   initializer = box.store, 1
    # example encode call with initializer :
    #   box_encoded_initializer_function = encode_function_data(initializer)
    box_encoded_initializer_function = encode_function_data()

    # deploying the proxy contract
    proxy = BoxProxy.deploy(
        box.address,
        box_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy.address}")

    # Assigning the proxy contract to have the Box.ABI
    # Should allow calling of the Box functions on the contract at proxy.address
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(27, {"from": account})
    print(proxy_box.retrieve())  # returns 27

    box_v2 = BoxV2.deploy({"from": account})

    # upgrades the proxy code to point to the implementation at box_v2.address and thus allows increment() function to be called.
    upgrade(account, proxy, box_v2.address, proxy_admin=box_admin)

    print(f"Proxy implementation has been upgraded to {box_v2.address}")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    tx = proxy_box.increment({"from": account})
    tx.wait(1)
    print(
        proxy_box.retrieve()
    )  # returns 28 as the previous state is kept after the upgrade
