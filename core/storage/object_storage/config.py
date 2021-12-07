from betterconf import Config, field


class S3Connect(Config):
    url = field("S3_URL", default="http://172.5.0.5:9000")
    password = field("PASSWORD", default="minio123")
    login = field("LOGIN", default="minio")


config = S3Connect()
