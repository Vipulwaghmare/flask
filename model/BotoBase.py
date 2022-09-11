import json
import boto3

class BotoBase:
  def __init__(self):
    self.load_config_base()

  def load_config_base(self):
    with open('settings/boto_base_config.json') as config_file:
      config_data = json.load(config_file)
      self._aws_access_key_id = config_data['aws_access_key_id']
      self._aws_secret_access_key = config_data["aws_secret_access_key"]
      self._aws_region_name = config_data["aws_region_name"]

  def init_client(self, service_name):
    try:
      if hasattr(self, '_base_url'):
        self._client = boto3.client(
            service_name,
            aws_access_key_id = self._aws_access_key_id,
            aws_secret_access_key = self._aws_secret_access_key,
            region_name = self._aws_region_name,
            endpoint_url = self._base_url
        )
      else:
        self._client = boto3.client(
            service_name,
            aws_access_key_id = self._aws_access_key_id,
            aws_secret_access_key = self._aws_secret_access_key,
            region_name = self._aws_region_name
        )
    except Exception as e:
      raise e