import os
from model.BotoBase import BotoBase
from botocore.exceptions import ClientError
from flask import send_file
from model.LambdaPDF import LambdaPDF
from utils.helpers import Wrapper_For_Read

class BotoS3(BotoBase):
  def __init__(self):
    super().__init__()
    service_name = 's3'
    self.init_client(service_name)

  def get_file(self, file_name, bucket_name):
    try:
      file = self._client.get_object(Bucket=bucket_name, Key=file_name)
    except Exception as e:
      raise e
    return file

  def send_file_in_response(self, file_name, bucket_name):
    try:
      file = self.get_file(Bucket=bucket_name, Key=file_name)
      file_content = file['Body']
      # file_content = file['Body'].read()
    except Exception as e:
      raise e
    return send_file(file_content, mimetype='multipart/form-data', as_attachment=True, attachment_filename= 'fileName.pdf')

  def save_file_to_s3(self, fileObj, bucket, key):
    # file = request.files['file']
    # filename = file.filename
    # fileObj = file
    try:
      self._client.upload_fileobj(fileObj, bucket, key)
    except Exception as e:
      raise e
    return True
  
  def save_file_to_s3_by_local(self, file, bucket, key):
    try:
      UPLOAD_FOLDER = "./TEMP/"
      file_path = UPLOAD_FOLDER + file.filename
      file.save(file_path)
      self._client.upload_file(file_path, bucket, key)
      os.remove(file_path)
    except Exception as e:
      raise e
    return True

  def convert_html_to_pdf_and_save(self, html):
    try:
      lambda_pdf = LambdaPDF()
      pdf_blob = lambda_pdf(html)
    except Exception as e:
      print("Failed to get pdf from lambda")
      raise e 
    try:
      pdf_blob = Wrapper_For_Read(pdf_blob)
      self.save_file_to_s3(pdf_blob, "filename.pdf")
    except Exception as e:
      print("Failed to save file")
      raise e 
    return True

  def get_list_of_files(self, bucket_name, prefix):
    try:
      response = self._client.list_objects(Bucket=bucket_name, Prefix=prefix)
    except Exception as e:
      raise e
    return response
        
  def get_list_of_files_v2(self, bucket_name, prefix):
    try:
      response = self._client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    except Exception as e:
      raise e
    return response
       
  def delete_object(self, bucket_name, key):
    try:
      response = self._client.delete_object(Bucket = bucket_name, Key = key)
    except Exception as e:
      raise e
    return response