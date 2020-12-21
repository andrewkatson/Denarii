#!/usr/bin/env python3
#encoding=utf-8

# Copyright (c) 2019-2020 The Monero Project
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Test basic wallet functionality
"""

from __future__ import print_function
import sys
import os
import errno

from framework.wallet import Wallet
from framework.daemon import Daemon

class WalletTest():
    def run_test(self):
      self.reset()
      self.create()
      self.check_main_address()
      self.check_keys()
      self.create_subaddresses()
      self.tags()
      self.attributes()
      self.open_close()
      self.languages()
      self.change_password()
      self.store()

    def remove_file(self, name):
        WALLET_DIRECTORY = os.environ['WALLET_DIRECTORY']
        assert WALLET_DIRECTORY != ''
        try:
            os.unlink(WALLET_DIRECTORY + '/' + name)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def remove_wallet_files(self, name):
        for suffix in ['', '.keys']:
            self.remove_file(name + suffix)

    def file_exists(self, name):
        WALLET_DIRECTORY = os.environ['WALLET_DIRECTORY']
        assert WALLET_DIRECTORY != ''
        return os.path.isfile(WALLET_DIRECTORY + '/' + name)

    def reset(self):
        print('Resetting blockchain')
        daemon = Daemon()
        res = daemon.get_height()
        daemon.pop_blocks(res.height - 1)
        daemon.flush_txpool()

    def create(self):
        print('Creating wallet')
        wallet = Wallet()
        # close the wallet if any, will throw if none is loaded
        try: wallet.close_wallet()
        except: pass
        seed = 'donuts casket wives dice shipped token goblet zippers makeup ladder sincerely dice elbow suede gown heels vessel entrance moon today refer limits often pests wives'
        res = wallet.restore_deterministic_wallet(seed = seed)
        print(res.address)
        assert res.address == '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b'
        assert res.seed == seed

    def check_main_address(self):
        print('Getting address')
        wallet = Wallet()
        res = wallet.get_address()
        assert res.address == '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b', res
        assert len(res.addresses) == 1
        assert res.addresses[0].address == res.address
        assert res.addresses[0].address_index == 0
        assert res.addresses[0].used == False

    def check_keys(self):
        print('Checking keys')
        wallet = Wallet()
        res = wallet.query_key('view_key')
        assert res.key == '65b84da608e32042dde1648ea8240fa963c9e6943da69396be9793b7f7394209'
        res = wallet.query_key('spend_key')
        assert res.key == '0a8cadd59f300b1824b1bc855823356bd2a78189a4202353a4330cd9541b4f0c'
        res = wallet.query_key('mnemonic')
        assert res.key == 'donuts casket wives dice shipped token goblet zippers makeup ladder sincerely dice elbow suede gown heels vessel entrance moon today refer limits often pests wives'

    def create_subaddresses(self):
        print('Creating subaddresses')
        wallet = Wallet()
        res = wallet.create_account("idx1")
        assert res.account_index == 1, res
        assert res.address == 'F9yzrvYc5TZXBXyZgmYh7A3qRF8XKsrgdg4dv3SdVQTPaj6x23gijwFYKwCfN1fHNCVFEK6zNCA5ehQJaYNEYhwQNjGXCvW', res
        res = wallet.create_account("idx2")
        assert res.account_index == 2, res
        assert res.address == 'F9XX3hoafehehoxjJLSzJ1HxBTmwffzBsXR6RfbvB8wm6ZLi9GbnbfpDivUZYMpNx1fggniLqmL9MDQewjsLUtfNEE4nLZC', res

        res = wallet.get_address(0, 0)
        assert res.address == '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b', res
        assert len(res.addresses) == 1
        assert res.addresses[0].address_index == 0, res
        res = wallet.get_address(1, 0)
        assert res.address == 'F9yzrvYc5TZXBXyZgmYh7A3qRF8XKsrgdg4dv3SdVQTPaj6x23gijwFYKwCfN1fHNCVFEK6zNCA5ehQJaYNEYhwQNjGXCvW', res
        assert len(res.addresses) == 1
        assert res.addresses[0].label == 'idx1', res
        assert res.addresses[0].address_index == 0, res
        res = wallet.get_address(2, 0)
        assert res.address == 'F9XX3hoafehehoxjJLSzJ1HxBTmwffzBsXR6RfbvB8wm6ZLi9GbnbfpDivUZYMpNx1fggniLqmL9MDQewjsLUtfNEE4nLZC', res
        assert len(res.addresses) == 1
        assert res.addresses[0].label == 'idx2', res
        assert res.addresses[0].address_index == 0, res

        res = wallet.create_address(0, "sub_0_1")
        res = wallet.create_address(1, "sub_1_1")
        res = wallet.create_address(1, "sub_1_2")

        res = wallet.get_address(0, [1])
        assert len(res.addresses) == 1
        assert res.addresses[0].address == 'F9n8FAPf2PEdwjgephXqsy5z5PUVpoYsJ16Tcq78riJNEaEdbr8kfqRjTjC2iCDuiK3Lg5N85LXz67LeW7ei4uAJTgmviM1'
        assert res.addresses[0].label == 'sub_0_1'
        res = wallet.get_address(1, [1])
        assert len(res.addresses) == 1
        assert res.addresses[0].address == 'F6DtFZcLw6yWMYKNUCNJfp13W9dnyoHsGCEbqZyC13HsYMDTxxW74rEMsfFUUCwN24fvgPFVgWWgs1WaKy2uCemaJCd2Mzz'
        assert res.addresses[0].label == 'sub_1_1'
        res = wallet.get_address(1, [2])
        assert len(res.addresses) == 1
        assert res.addresses[0].address == 'FAwZhKPYptpMxuGLmMxHrUd5SwzHRMQw9DT1dhTNtDgzTs8FFHcbyYQHXJwwip32V56BmKkRNV72dMnoGPCjo3ieH3GQXsL'
        assert res.addresses[0].label == 'sub_1_2'
        res = wallet.get_address(1, [0, 1, 2])
        assert len(res.addresses) == 3
        assert res.addresses[0].address == 'F9yzrvYc5TZXBXyZgmYh7A3qRF8XKsrgdg4dv3SdVQTPaj6x23gijwFYKwCfN1fHNCVFEK6zNCA5ehQJaYNEYhwQNjGXCvW'
        assert res.addresses[0].label == 'idx1'
        assert res.addresses[1].address == 'F6DtFZcLw6yWMYKNUCNJfp13W9dnyoHsGCEbqZyC13HsYMDTxxW74rEMsfFUUCwN24fvgPFVgWWgs1WaKy2uCemaJCd2Mzz'
        assert res.addresses[1].label == 'sub_1_1'
        assert res.addresses[2].address == 'FAwZhKPYptpMxuGLmMxHrUd5SwzHRMQw9DT1dhTNtDgzTs8FFHcbyYQHXJwwip32V56BmKkRNV72dMnoGPCjo3ieH3GQXsL'
        assert res.addresses[2].label == 'sub_1_2'

        res = wallet.label_address((1, 2), "sub_1_2_new")
        res = wallet.get_address(1, [2])
        assert len(res.addresses) == 1
        assert res.addresses[0].address == 'FAwZhKPYptpMxuGLmMxHrUd5SwzHRMQw9DT1dhTNtDgzTs8FFHcbyYQHXJwwip32V56BmKkRNV72dMnoGPCjo3ieH3GQXsL'
        assert res.addresses[0].label == 'sub_1_2_new'

        res = wallet.label_account(1, "idx1_new")
        res = wallet.get_address(1, [0])
        assert len(res.addresses) == 1
        print(res.addresses[0].address)
        assert res.addresses[0].address == 'F9yzrvYc5TZXBXyZgmYh7A3qRF8XKsrgdg4dv3SdVQTPaj6x23gijwFYKwCfN1fHNCVFEK6zNCA5ehQJaYNEYhwQNjGXCvW'
        assert res.addresses[0].label == 'idx1_new'

        res = wallet.get_address_index('FAwZhKPYptpMxuGLmMxHrUd5SwzHRMQw9DT1dhTNtDgzTs8FFHcbyYQHXJwwip32V56BmKkRNV72dMnoGPCjo3ieH3GQXsL')
        assert res.index == {'major': 1, 'minor': 2}
        res = wallet.get_address_index('76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b')
        assert res.index == {'major': 0, 'minor': 0}
        res = wallet.get_address_index('F9n8FAPf2PEdwjgephXqsy5z5PUVpoYsJ16Tcq78riJNEaEdbr8kfqRjTjC2iCDuiK3Lg5N85LXz67LeW7ei4uAJTgmviM1')
        assert res.index == {'major': 0, 'minor': 1}
        res = wallet.get_address_index('F9yzrvYc5TZXBXyZgmYh7A3qRF8XKsrgdg4dv3SdVQTPaj6x23gijwFYKwCfN1fHNCVFEK6zNCA5ehQJaYNEYhwQNjGXCvW')
        assert res.index == {'major': 1, 'minor': 0}

        res = wallet.label_account(0, "main")

    def tags(self):
        print('Testing tags')
        wallet = Wallet()
        res = wallet.get_account_tags()
        assert not 'account_tags' in res or len(res.account_tags) == 0
        ok = False
        try: res = wallet.get_accounts('tag')
        except: ok = True
        assert ok or not 'subaddress_accounts' in res or res.subaddress_accounts == 0
        wallet.tag_accounts('tag0', [1])
        res = wallet.get_account_tags()
        assert len(res.account_tags) == 1
        assert res.account_tags[0].tag == 'tag0'
        assert res.account_tags[0].label == ''
        assert res.account_tags[0].accounts == [1]
        res = wallet.get_accounts('tag0')
        assert len(res.subaddress_accounts) == 1
        assert res.subaddress_accounts[0].account_index == 1
        assert res.subaddress_accounts[0].base_address == 'F9yzrvYc5TZXBXyZgmYh7A3qRF8XKsrgdg4dv3SdVQTPaj6x23gijwFYKwCfN1fHNCVFEK6zNCA5ehQJaYNEYhwQNjGXCvW'
        assert res.subaddress_accounts[0].balance == 0
        assert res.subaddress_accounts[0].unlocked_balance == 0
        assert res.subaddress_accounts[0].label == 'idx1_new'
        assert res.subaddress_accounts[0].tag == 'tag0'
        wallet.untag_accounts([0])
        res = wallet.get_account_tags()
        assert len(res.account_tags) == 1
        assert res.account_tags[0].tag == 'tag0'
        assert res.account_tags[0].label == ''
        assert res.account_tags[0].accounts == [1]
        wallet.untag_accounts([1])
        res = wallet.get_account_tags()
        assert not 'account_tags' in res or len(res.account_tags) == 0
        wallet.tag_accounts('tag0', [0])
        wallet.tag_accounts('tag1', [1])
        res = wallet.get_account_tags()
        assert len(res.account_tags) == 2
        x = [x for x in res.account_tags if x.tag == 'tag0']
        assert len(x) == 1
        assert x[0].tag == 'tag0'
        assert x[0].label == ''
        assert x[0].accounts == [0]
        x = [x for x in res.account_tags if x.tag == 'tag1']
        assert len(x) == 1
        assert x[0].tag == 'tag1'
        assert x[0].label == ''
        assert x[0].accounts == [1]
        wallet.tag_accounts('tagA', [0, 1])
        res = wallet.get_account_tags()
        assert len(res.account_tags) == 1
        assert res.account_tags[0].tag == 'tagA'
        assert res.account_tags[0].label == ''
        assert res.account_tags[0].accounts == [0, 1]
        wallet.tag_accounts('tagB', [1, 0])
        res = wallet.get_account_tags()
        assert len(res.account_tags) == 1
        assert res.account_tags[0].tag == 'tagB'
        assert res.account_tags[0].label == ''
        assert res.account_tags[0].accounts == [0, 1]
        wallet.set_account_tag_description('tagB', 'tag B')
        res = wallet.get_account_tags()
        assert len(res.account_tags) == 1
        assert res.account_tags[0].tag == 'tagB'
        assert res.account_tags[0].label == 'tag B'
        assert res.account_tags[0].accounts == [0, 1]
        res = wallet.get_accounts('tagB')
        assert len(res.subaddress_accounts) == 2
        subaddress_accounts = []
        for x in res.subaddress_accounts:
            assert x.balance == 0
            assert x.unlocked_balance == 0
            subaddress_accounts.append((x.account_index, x.base_address, x.label))
        assert sorted(subaddress_accounts) == [(0, '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b', 'main'), (1, 'F9yzrvYc5TZXBXyZgmYh7A3qRF8XKsrgdg4dv3SdVQTPaj6x23gijwFYKwCfN1fHNCVFEK6zNCA5ehQJaYNEYhwQNjGXCvW', 'idx1_new')]

    def attributes(self):
        print('Testing attributes')
        wallet = Wallet()

        ok = False
        try: res = wallet.get_attribute('foo')
        except: ok = True
        assert ok
        res = wallet.set_attribute('foo', 'bar')
        res = wallet.get_attribute('foo')
        assert res.value == 'bar'
        res = wallet.set_attribute('foo', 'いっしゅん')
        res = wallet.get_attribute('foo')
        assert res.value == u'いっしゅん'
        ok = False
        try: res = wallet.get_attribute('いちりゅう')
        except: ok = True
        assert ok
        res = wallet.set_attribute('いちりゅう', 'いっぽう')
        res = wallet.get_attribute('いちりゅう')
        assert res.value == u'いっぽう'

    def open_close(self):
        print('Testing open/close')
        wallet = Wallet()

        res = wallet.get_address()
        assert res.address == '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b'

        wallet.close_wallet()
        ok = False
        try: res = wallet.get_address()
        except: ok = True
        assert ok

        wallet.restore_deterministic_wallet(seed = 'loyal poetry byline espionage thorn tossed ugly peeled bailed saved necklace silk mobile newt envy slug claim family loincloth innocent people apology niche opus ugly')
        res = wallet.get_address()
        assert res.address == '79DtEURvmq8dW2M5x8A9Lo6VNCJgkUPQv8M4r17YURgTF8NRA8E5XKCRQ4rwSSbiEDHbXByefuWpDcn5h257zwuyRX6uhhT'

        wallet.close_wallet()
        ok = False
        try: wallet.get_address()
        except: ok = True
        assert ok

        wallet.restore_deterministic_wallet(seed = 'donuts casket wives dice shipped token goblet zippers makeup ladder sincerely dice elbow suede gown heels vessel entrance moon today refer limits often pests wives')
        res = wallet.get_address()
        assert res.address == '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b'

    def languages(self):
        print('Testing languages')
        wallet = Wallet()
        res = wallet.get_languages()
        assert 'English' in res.languages
        assert 'English' in res.languages_local
        assert 'Dutch' in res.languages
        assert 'Nederlands' in res.languages_local
        assert 'Japanese' in res.languages
        assert u'日本語' in res.languages_local
        try: wallet.close_wallet()
        except: pass
        languages = res.languages
        languages_local = res.languages_local
        for language in languages + languages_local:
            sys.stdout.write('Creating ' + language + ' wallet\n')
            wallet.create_wallet(filename = '', language = language)
            res = wallet.query_key('mnemonic')
            wallet.close_wallet()

    def change_password(self):
        print('Testing password change')
        wallet = Wallet()

        # close the wallet if any, will throw if none is loaded
        try: wallet.close_wallet()
        except: pass

        self.remove_wallet_files('test1')

        seed = 'donuts casket wives dice shipped token goblet zippers makeup ladder sincerely dice elbow suede gown heels vessel entrance moon today refer limits often pests wives'
        res = wallet.restore_deterministic_wallet(seed = seed, filename = 'test1')
        print(res)
        assert res.address == '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b'
        assert res.seed == seed

        wallet.close_wallet()
        res = wallet.open_wallet('test1', password = '')
        print(res)
        res = wallet.get_address()
        print(res)
        assert res.address == '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b'

        res = wallet.change_wallet_password(old_password = '', new_password = 'foo')
        print(res)
        print("RESULT OF CHANGING " + str(res))
        wallet.close_wallet()

        ok = False
        try: res = wallet.open_wallet('test1', password = '')
        except: ok = True
        assert ok

        res = wallet.open_wallet('test1', password = 'foo')
        print(res)
        res = wallet.get_address()
        print(res)
        assert res.address == '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b'

        wallet.close_wallet()

        self.remove_wallet_files('test1')

    def store(self):
        print('Testing store')
        wallet = Wallet()

        # close the wallet if any, will throw if none is loaded
        try: wallet.close_wallet()
        except: pass

        self.remove_wallet_files('test1')

        seed = 'donuts casket wives dice shipped token goblet zippers makeup ladder sincerely dice elbow suede gown heels vessel entrance moon today refer limits often pests wives'
        res = wallet.restore_deterministic_wallet(seed = seed, filename = 'test1')
        assert res.address == '76YmRQ6ZLq4Ge17ryYXF83HthNRvc1uHARYQg2AkoYhdNL7u1kBNiXFJrnSskFi9fNbPkjh3tQ7fv87NKVmpxKVwFyURn1b'
        assert res.seed == seed

        self.remove_file('test1')
        assert self.file_exists('test1.keys')
        assert not self.file_exists('test1')
        wallet.store()
        assert self.file_exists('test1.keys')
        assert self.file_exists('test1')

        wallet.close_wallet()
        self.remove_wallet_files('test1')


if __name__ == '__main__':
    WalletTest().run_test()
