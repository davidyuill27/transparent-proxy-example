from brownie import Box, BoxV2, BoxAdmin, BoxProxy
from brownie.network.contract import Contract
from scripts.account_utils import encode_function_data, get_account


def test_proxy_delegates_calls():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = BoxAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()

    proxy = BoxProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    assert proxy_box.retrieve() == 0
    proxy_box.store(27, {"from": account})
    assert proxy_box.retrieve() == 27
