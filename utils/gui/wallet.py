

class Wallet:

    def __init__(self, address=None, name=None, password=None, phrase=None, sub_addressees=None):

        self.address = address
        self.name = name
        self.password = password
        self.phrase = phrase
        self.sub_addresses = []
