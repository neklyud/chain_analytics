from betterconf import Config, field
from betterconf.caster import to_int


class Configuration(Config):
    class RabbitMQConfig(Config):
        url: str = field("RABBIT_URL", default="localhost")
        port: int = field("RABBIT_PORT", caster=to_int, default=5672)
        password: str = field("RABBIT_PASSWORD", default="12345")
        login: str = field("RABBIT_LOGIN", default="user")
        web2loader_queue_name: str = field("web2loader_queue_name", default="web2loader_queue")


config = Configuration()
