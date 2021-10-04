from brownie import (
    network,
    accounts,
    config,
)
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVINROMENTS = ["development", "ganache-local"]

# Util function to get account depending on network used
def get_account(index=None, id=None):

    if index:
        return accounts[index]
    if id:
        accounts.load(id)
    if local_network_check():
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


def local_network_check():
    """
    Checks if the network is running locally or not (Either forked or local ganache)
    """
    return (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVINROMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    )


def encode_function_data(initializer=None, *args):
    """
    Encodes the given arguments for the initializer to a hex string
    """
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account, proxy, new_impl_address, proxy_admin=None, initializer=None, *args
):
    # if the proxy is owned by the proxy admin
    if proxy_admin:
        # if there is an initializer for the new implementation
        if initializer:
            encode_function_data = encode_function_data(initializer, args)
            tx = proxy_admin.upgradeAndCall(
                proxy.address, new_impl_address, encode_function_data, {"from": account}
            )
        # just upgrade to new implementation with no init
        else:
            tx = proxy_admin.upgrade(proxy.address, new_impl_address, {"from": account})
    # if the proxy is owned by the usual EOA
    else:
        # if there is an initializer for the new implementation
        if initializer:
            encode_function_data = encode_function_data()
            tx = proxy.upgradeToAndCall(
                new_impl_address, encode_function_data, {"from": account}
            )
        # just upgrade to new implementation with no init
        else:
            tx = proxy.upgradeTo(new_impl_address, {"from": account})

    return tx
