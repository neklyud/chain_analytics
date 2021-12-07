from betterconf.config import Config, field


class MoralisLoader(Config):
    class MoralisApi(Config):
        server_url = field("server_api", default="https://iq5jnlm0hohk.usemoralis.com:2053/server")
        application_id = field("application_id", default="gd0RL7naCkzdeVMK41xGOPBVbVnS0Ib0I9BrsPxn")
        master_key = field("master_key", default="UZUxqyEp7Ilc0IaqAKGRP7gUs9QE5x6sk9RWEAnN")


config = MoralisLoader()
