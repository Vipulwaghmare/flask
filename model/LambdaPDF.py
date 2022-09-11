import pycurl
import json

class LambdaPDF:
  def __init__(self):
    # URL which returns empty object
    self.lambdaUrl = "http://localhost:3000/empty-obj"
    self.headers = ["Content-type: application/json"]

  def getPdfFromHTML(self, html, raw=False):
    try:
      curl = pycurl.Curl()
      curl.setopt(pycurl.POST, True)
      curl.setopt(pycurl.HTTPHEADER, self.headers)
      curl.setopt(curl.POSTFIELDS,  json.dumps({"html": html}) )
      curl.setopt(curl.URL, self.lambdaUrl)
      result = curl.perform_rs()
      curl.close()
    except Exception as e:
      raise e

    try:
      response = json.loads(result)
      pdfBytes = bytes.fromhex(response["blob"]) if not raw else response["blob"]
    except Exception as e:
      raise e
    return pdfBytes