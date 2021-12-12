from betterconf import Config, field


class Web3LoaderService(Config):
    service_config = field("SERVICE_CONFIG", default="factory.json")


config = Web3LoaderService()
