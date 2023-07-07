from wallet_screen import *


class RemoteWalletScreen(WalletScreen):
    """
    A screen that allows the user to interact with a remote wallet. Aka one that allows the buying and selling of
    denarii and stores the data in the cloud.
    """

    def __init__(self, main_layout, deletion_func, denarii_client, gui_user, denarii_mobile_client, **kwargs):
        super().__init__(main_layout=main_layout, deletion_func=deletion_func, denarii_client=denarii_client,
                         gui_user=gui_user, suffix=self.remote_wallet_suffix, denarii_mobile_client=denarii_mobile_client, **kwargs)

    def init(self, **kwargs):
        super().init(**kwargs)

        self.wallet = kwargs['remote_wallet']

    def setup(self):
        super().setup()

    def teardown(self):
        super().teardown()

    def populate_wallet_screen(self):
        """
        Populate the wallet scene with user wallet information
        """

        super().populate_wallet_screen()
