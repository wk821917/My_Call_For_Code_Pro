import ibm_boto3
from ibm_botocore.client import Config
import os
import re

if not os.path.exists('./downloadfile'): os.mkdir('./downloadfile')

cos_credentials = {
  "apikey": "eUU7ks-YstaFkkEjoIVEsUkvU2_mUq-tcwfyQamY6kim",
  "cos_hmac_keys": {
    "access_key_id": "f1ac76f0074244f9a07d5debb286f122",
    "secret_access_key": "c623bb131af41897c674eec7f7700446fdbeecf6c993d105"
  },
  "endpoints": "https://cos-service.bluemix.net/endpoints",
  "iam_apikey_description": "Auto generated apikey during resource-key operation for Instance - crn:v1:bluemix:public:cloud-object-storage:global:a/4171c5a3fdf4490ba445218f5bcdea3a:ddbf4da0-34e3-4055-aba2-6b23b0b2b78b::",
  "iam_apikey_name": "auto-generated-apikey-f1ac76f0-0742-44f9-a07d-5debb286f122",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/4171c5a3fdf4490ba445218f5bcdea3a::serviceid:ServiceId-ed5194dd-dab1-411b-b53c-df5f95c3d594",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/4171c5a3fdf4490ba445218f5bcdea3a:ddbf4da0-34e3-4055-aba2-6b23b0b2b78b::"
}

api_key = cos_credentials['apikey']
service_instance_id = cos_credentials['resource_instance_id']

service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
cos = ibm_boto3.resource ('s3',
                         ibm_api_key_id=api_key,
                         ibm_service_instance_id=service_instance_id,
                         ibm_auth_endpoint=auth_endpoint,
                         config=Config(signature_version='oauth'),
                         endpoint_url=service_endpoint)
print('--------list all buckets--------')
print(list(cos.buckets.all()))

name = 'history'
bucket_obj = cos.Bucket(name)
files = bucket_obj.objects.all()
for file in files:
    dirname = re.sub("\D","",file.key)
    if not os.path.exists("./downloadfile/data"+dirname): os.mkdir("./downloadfile/data"+dirname)
    if not os.path.exists("./downloadfile/data"+dirname+'/'+file.key):
        bucket_obj.download_file(file.key, './downloadfile/data'+dirname+"/"+file.key)
    	print('-------download '+file.key+'-------')
