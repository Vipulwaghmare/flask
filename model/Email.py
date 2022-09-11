import json
from smtplib import SMTP_SSL as SMTP
from string import Template
from templates.emails.email_templates import email_templates
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class Email:
  def __init__(self):
    self.load_config()
  
  def load_config(self):
    config_file_name = "email_config"
    file_path = "settings/{}.json".format(config_file_name)
    with open(file_path) as config_file:
      config_data = json.load(config_file)
      self._smtp_host = config_data["smtp_host"]
      self._sender = config_data["sender"]
      self._user_name = config_data["user_name"]
      self._password = config_data["password"]
      self._qa_email = config_data["qa_email"]
      self._white_list = config_data["white_list"]
    
  # Parameters
  # @ data['destination'] => string => Email Receiver
  # @ data['subject'] => string => Email Subject
  # @ data['template'] => string => Name of the template to use
  # @ data['substitute'] => dict => data to map in the template
  def send_email(self, data, attachment = None):
    smtp_host = self._smtp_host
    sender = self._sender
    user_name = self._user_name
    password = self._password

    try:
      (destination, subject, template, sub) = (data['destination'], data['subject'], data['template'], data['substitute'])
    except Exception as e:
      raise e
    
    try:
      template = Template(email_templates[template])
      content = template.safe_substitute(sub)
    except Exception as e:
      raise e
    
    try:
      conn = SMTP(smtp_host)
      msg = MIMEMultipart()
      msg.attach(MIMEText(content, 'html'))
      msg['Subject'] = subject
      msg['From'] = sender
      msg['To'] = destination
      if attachment:
          filename = data['substitute']['filename']
          fileExt = filename.split('.')[1]
          att = MIMEApplication(attachment, str(fileExt))
          att.add_header('Content-Disposition','attachment',filename=filename)
          msg.attach(att)

      conn.set_debuglevel(False)
      conn.login(user_name, password)
      conn.sendmail(sender, destination, msg.as_string())
    except Exception as e:
      raise e
    finally:
      conn.quit()