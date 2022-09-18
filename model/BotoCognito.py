from model.BotoBase import BotoBase
import json

class BotoCognito(BotoBase):
  def __init__(self):
    super().__init__()
    service_name = "cognito-idp"
    self.load_config_base()
    self.init_client(service_name)

  def load_config_base(self):
    with open('settings/boto_config.json') as config_file:
      config_data = json.load(config_file)
      self._user_pool_id = config_data['user_pool_id']
      self._client_id = config_data["client_id"]
      self._client_secret = config_data["client_secret"]
  
  def initiate_auth(self, username, password):
    pass