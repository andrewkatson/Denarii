from wallet import * 

class GuiUser: 

    def __init__(self, name=None, email=None, password=None, local_wallet=None, remote_wallet=None, language=None):
        self.name = name
        self.email = email
        self.password = password
        self.local_wallet = local_wallet
        self.remote_wallet = remote_wallet
        self.language = language

    def __str__(self): 
        return f"{self.name}:{self.email}:{self.language}"
