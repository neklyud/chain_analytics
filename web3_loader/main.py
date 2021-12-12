from core.configs.service_config import ServiceConfig, load_config
from web3_loader.config import config
from core.factory.meta_factory import get_factory


if __name__ == '__main__':
    service_config = load_config(config.service_config)
    print(service_config)
    factory = get_factory(service_config)
    print(dir(factory))
