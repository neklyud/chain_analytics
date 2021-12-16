from betterconf import Config, field


class Web3LoaderService(Config):
    service_config = field("SERVICE_CONFIG", default="factory.json")

    class Providers(Config):
        mainnet_infura = field("MAINNET_INFURA",
                               default="https://mainnet.infura.io/v3/64df41bec1504ebc9dea88b8f4c595a7")


config = Web3LoaderService()
