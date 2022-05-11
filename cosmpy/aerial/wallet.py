# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Optional

from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

from cosmpy.crypto.address import Address
from cosmpy.crypto.hashfuncs import sha256
from cosmpy.crypto.interface import Signer
from cosmpy.crypto.keypairs import PrivateKey, PublicKey


class Wallet(ABC):
    @abstractmethod
    def address(self) -> Address:
        pass

    @abstractmethod
    def public_key(self) -> PublicKey:
        pass

    @abstractmethod
    def signer(self) -> Signer:
        pass


class LocalWallet(Wallet):
    @staticmethod
    def generate() -> "LocalWallet":
        return LocalWallet(PrivateKey())

    @staticmethod
    def from_mnemonic(mnemonic: str) -> "LocalWallet":
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        bip44_def_ctx = Bip44.FromSeed(
            seed_bytes, Bip44Coins.COSMOS
        ).DeriveDefaultPath()
        return LocalWallet(PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes()))

    @staticmethod
    def from_unsafe_seed(text: str, index: Optional[int] = None) -> "LocalWallet":
        private_key_bytes = sha256(text.encode())
        if index is not None:
            private_key_bytes = sha256(
                private_key_bytes + index.to_bytes(4, byteorder="big")
            )
        return LocalWallet(PrivateKey(private_key_bytes))

    def __init__(self, private_key: PrivateKey):
        self._private_key = private_key

    def address(self) -> Address:
        return Address(self._private_key)

    def public_key(self) -> PublicKey:
        return self._private_key

    def signer(self) -> PrivateKey:
        return self._private_key
