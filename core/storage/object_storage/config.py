from betterconf import Config, field


class S3Connect(Config):
    url = field("S3_URL", default="http://127.0.0.1:9000")
    password = field("PASSWORD", default="AKIAIOSFODNN7EXAMPLE")
    login = field("LOGIN", default="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")


config = S3Connect()
