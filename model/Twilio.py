import json
from twilio.rest import Client

class Twilio:
  def __init__(self):
    self.load_config()
      
  def load_config(self):
    file_path = f"settings/twilio_config.json"
    with open(file_path) as config_file:
      config_data = json.load(config_file)
      self._account_sid = config_data['account_sid']
      self._auth_token = config_data['auth_token']
      self._from = config_data['from']
      self._client = Client(self._account_sid, self._auth_token)

  def send_message(self, to_number, body):
    message = self._client.messages.create(
        from_ = self._from,
        body= body,
        to = to_number
    )
    return message.sid