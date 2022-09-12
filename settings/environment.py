import os
env = os.environ.get("API_ENV", default="LOCAL")

if env == "PROD":
  config_folder = "prod"
elif env == "LOCAL":
  config_folder = "local"