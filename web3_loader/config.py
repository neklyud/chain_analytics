from betterconf import Config, field


class Web3LoaderService(Config):
    service_config = field("SERVICE_CONFIG", default="factory.json")

    class S3(Config):
        web3_s3_bucket = field("WEB3_S3_BUCKET", default="web3")

    class Providers(Config):
        mainnet_infura = field("MAINNET_INFURA",
                               default="https://mainnet.infura.io/v3/64df41bec1504ebc9dea88b8f4c595a7")
        ropsten_infura = field("ROPSTEN_INFURA", default="https://ropsten.infura.io/v3/64df41bec1504ebc9dea88b8f4c595a7")


config = Web3LoaderService()
