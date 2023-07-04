from wallet_screen import *


class RemoteWalletScreen(WalletScreen):
    """
    A screen that allows the user to interact with a remote wallet. Aka one that allows the buying and selling of
    denarii and stores the data in the cloud.
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(main_layout, deletion_func, suffix=self.remote_wallet_suffix, **kwargs)

    def setup(self):
        super().setup()
