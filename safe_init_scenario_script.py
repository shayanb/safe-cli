#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.utils.build_contract_reader import ContractReader
from gnosis.eth.ethereum_client import EthereumClient
from gnosis.safe import Safe, ProxyFactory
from eth_account import Account
from gnosis.eth.contracts import (
    get_safe_contract, get_safe_V1_0_0_contract, get_safe_V0_0_1_contract
)



class ContractArtifact:
    def __init__(self, contract_name, contract_instance, contract_abi, contract_bytecode, contract_address):
        self.contract_name = contract_name
        self.contract_instance = contract_instance
        self.contract_abi = contract_abi
        self.contract_bytecode = contract_bytecode
        self.contract_address = contract_address
        self.data = {
            'name': self.contract_name,
            'instance': self.contract_instance,
            'abi': self.contract_abi,
            'bytecode': self.contract_bytecode,
            'address': self.contract_address
        }

# ethereum_client.w3.eth.contract(abi=safe_v101_abi, address=safe_v101_deployment_data.contract_address)

def gnosis_py_init_scenario():
    print('+' + '---------' * 10 + '+')
    print('Gnosis Py Init Scenario')
    print('+' + '---------' * 10 + '+')
    # Get new Ethereum Provider & ContractReader
    ethereum_client = EthereumClient()
    contract_reader = ContractReader()

    # Init Deployer Account
    local_account = Account.privateKeyToAccount('0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d')

    safe_v101_abi, safe_v101_bytecode, safe_v101 = contract_reader.read_from(
        './assets/contracts/safe/GnosisSafeV1.0.0.json')
    # safe_v100_abi, safe_v100_bytecode, safe_v100 = contract_reader.read_from('./assets/contracts/safe/GnosisSafeV1.0.0.json')
    # safe_v001_abi, safe_v001_bytecode, safe_v001 = contract_reader.read_from('./assets/contracts/safe/GnosisSafeV0.0.1.json')

    proxy_v101_abi, proxy_v101_bytecode, proxy_v101 = contract_reader.read_from(
        './assets/contracts/safe/ProxyFactoryV1.1.0.json')
    # proxy_v100_abi, proxy_v100_bytecode, proxy_v100 = contract_reader.read_from('./assets/contracts/safe/ProxyFactoryV1.0.0.json')

    # remark: Start Safe Contract Deployment
    proxy_v101_deployment_data = ProxyFactory.deploy_proxy_factory_contract(ethereum_client, local_account)
    print('Successfully Deployed', proxy_v101, 'with Address:', proxy_v101_deployment_data.contract_address)
    # proxy_v100_deployment_data = ProxyFactory.deploy_proxy_factory_contract_v1_0_0(ethereum_client, local_account)
    # print('Successfully Deployed', proxy_v100, 'with Address:', proxy_v100_deployment_data.contract_address)

    # remark: Start Safe Contract Deployment
    safe_v101_deployment_data = Safe.deploy_master_contract(ethereum_client, local_account)
    print('Successfully Deployed', safe_v101, 'with Address:', safe_v101_deployment_data.contract_address)
    # safe_v100_deployment_data = Safe.deploy_master_contract_v1_0_0(ethereum_client, local_account)
    # print('Successfully Deployed', safe_v100, 'with Address:', safe_v100_deployment_data.contract_address)
    # safe_v001_deployment_data = Safe.deploy_old_master_contract(ethereum_client, local_account)
    # print('Successfully Deployed', safe_v001, 'with Address:', safe_v001_deployment_data.contract_address)

    # remark: Setup for the Safe Contract
    threshold = 3
    owners = [ethereum_client.w3.eth.accounts[0], ethereum_client.w3.eth.accounts[1],
              ethereum_client.w3.eth.accounts[2]]
    ethereum_tx_sent = Safe.create(ethereum_client, local_account, safe_v101_deployment_data.contract_address, owners,
                                    threshold, proxy_factory_address=proxy_v101_deployment_data.contract_address)
    safe_v101_object = Safe(ethereum_tx_sent.contract_address, ethereum_client)
    print('compare:', ethereum_tx_sent.contract_address)
    # remark: Setup Another Safe Account
    # local_account1 = Account.privateKeyToAccount('0xadd53f9a7e588d003326d1cbf9e4a43c061aadd9bc938c843a79e7b4fd2ad743')
    # owners_aux = [ethereum_client.w3.eth.accounts[4], ethereum_client.w3.eth.accounts[5], ethereum_client.w3.eth.accounts[6], ethereum_client.w3.eth.accounts[7], ethereum_client.w3.eth.accounts[8]]
    # threshold_aux = 5
    # ethereum_tx_sent_aux = Safe.create(ethereum_client, local_account1, safe_v101_deployment_data.contract_address, owners_aux, threshold_aux, proxy_factory_address=proxy_v101_deployment_data.contract_address)
    # safe_v101_object_0 = Safe(ethereum_tx_sent_aux.contract_address, ethereum_client)
    # print('+' + '---------' * 10 + '+')
    # print('Test Address to loadContract --addres=%s' % (ethereum_tx_sent_aux.contract_address))
    # print('+' + '---------' * 10 + '+')

    # remark Loading Older Versions for the Safe Contract
    # ethereum_tx_sent1 = Safe.create(ethereum_client, local_account, safe_v100_deployment_data.contract_address, owners, threshold, proxy_factory_address=proxy_v100_deployment_data.contract_address)
    # safe_v100_object = Safe(ethereum_tx_sent1.contract_address, ethereum_client)

    # remark: Start Retrieving Instance for the Contract
    safe_v101_contract_instance = get_safe_contract(ethereum_client.w3, safe_v101_object.address)
    print('Successfully Retrieved', safe_v101, 'Contract Instance', safe_v101_contract_instance)
    # safe_v100_contract_instance = get_safe_V1_0_0_contract(ethereum_client.w3, safe_v100_object.address)
    # print('Successfully Retrieved', safe_v100, 'Contract Instance', safe_v100_contract_instance)
    # safe_v001_contract_instance = get_safe_V0_0_1_contract(ethereum_client.w3, gnosi_safe_address_v100)
    # print('Successfully Retrieved', safe_v001, 'Contract Instance', safe_v001_contract_instance)

    # remark: Test Commands For Each Safe Version 1.1.0
    print('+' + '---------' * 10 + '+')
    print(safe_v101_contract_instance.functions.NAME().call(), safe_v101_contract_instance.functions.VERSION().call())
    print(safe_v101_contract_instance.functions.isOwner(ethereum_client.w3.eth.accounts[0]).call())
    print(safe_v101_contract_instance.functions.getThreshold().call())
    print(safe_v101_contract_instance.functions.getOwners().call())
    print('+' + '---------' * 10 + '+')
    # (self, contract_name, contract_instance, contract_abi, contract_bytecode, contract_address):
    safe_v101_artifacts = ContractArtifact(safe_v101, safe_v101_contract_instance, safe_v101_abi, safe_v101_bytecode,
                                           safe_v101_object.address)

    return safe_v101_artifacts.data