from brownie import Box, BoxV2, BoxAdmin, BoxProxy, exceptions
from brownie.network.contract import Contract
from scripts.account_utils import encode_function_data, get_account, upgrade
import pytest


def test_upgrade():
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

    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    # assert that we can't call increment until upgrade has been done
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})

    upgrade(account, proxy, box_v2.address, proxy_admin=proxy_admin)
    assert proxy_box.retrieve() == 0
    tx = proxy_box.increment({"from": account})
    tx.wait(1)
    assert proxy_box.retrieve() == 1
