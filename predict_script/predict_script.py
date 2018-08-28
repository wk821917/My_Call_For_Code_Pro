import os
import time
import urllib
import zipfile
from zipfile import ZipFile
import shutil
import time

from watson_machine_learning_client import WatsonMachineLearningAPIClient
import ibm_boto3
from ibm_botocore.client import Config

error_flag = False

'''
config the wml and cos  
'''
wml_credentials = {
  "apikey": "pTnqNZ0XAffootUTOqc1XMomvp4I3EbyaSd8AkbiZ21g",
  "iam_apikey_description": "Auto generated apikey during resource-key operation for Instance - crn:v1:bluemix:public:pm-20:us-south:a/4171c5a3fdf4490ba445218f5bcdea3a:760eae04-56a0-43a8-b03b-f8debca2d81e::",
  "iam_apikey_name": "auto-generated-apikey-55cc61b4-90a1-41f0-b4a0-7804cdb95aa9",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/4171c5a3fdf4490ba445218f5bcdea3a::serviceid:ServiceId-ba4b4153-cba7-434c-996a-c29ee7de6c4d",
  "instance_id": "760eae04-56a0-43a8-b03b-f8debca2d81e",
  "password": "6c716585-43b5-40f3-8320-19cfd03b6247",
  "url": "https://us-south.ml.cloud.ibm.com",
  "username": "55cc61b4-90a1-41f0-b4a0-7804cdb95aa9"
}

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

url = 'https://github.com/wk821917/My_Call_For_Code_Pro/archive/master.zip'

client = WatsonMachineLearningAPIClient(wml_credentials)
print('----------------client version:------------------')
print(client.version)

if not cos.Bucket('history') in cos.buckets.all():
    print('Creating bucket "{}"...'.format('history'))
    try:
        cos.create_bucket(Bucket='history')
    except ibm_boto3.exceptions.ibm_botocore.client.ClientError as e:
        print('Error: {}.'.format(e.response['Error']['Message']))
print('-----------------list all buckets:-----------------')
print(list(cos.buckets.all()))

name = 'wktest2'
bucket_obj = cos.Bucket(name)

'''
get the training-id when the model trained like 'training-o3hdtoFiR'
'''
bucket_obj.download_file('training-o3hdtoFiR/model/lstm.json', './lstm.json')
bucket_obj.download_file('training-o3hdtoFiR/weight/weight.hdf5', './weight.hdf5')
print('--------------download model and weight completed------------------')

urllib.request.urlretrieve(url, './master.zip')
print('----------------download file from github completed-----------------')

z = ZipFile('./master.zip')
if not os.path.exists('./My_Call_For_Code_Pro-master'): os.mkdir('./My_Call_For_Code_Pro-master')
z.extractall('./My_Call_For_Code_Pro-master')

shutil.copyfile('./lstm.json','./My_Call_For_Code_Pro-master/My_Call_For_Code_Pro-master/lstm.json')
os.remove('./lstm.json')
shutil.copyfile('./weight.hdf5','./My_Call_For_Code_Pro-master/My_Call_For_Code_Pro-master/weight.hdf5')
os.remove('./weight.hdf5')
shutil.copyfile('./last_time.json','./My_Call_For_Code_Pro-master/My_Call_For_Code_Pro-master/last_time.json')


print('--------------ziping the files into the train path-----------')
def zip_ya(startdir,file_news):
    z = ZipFile(file_news,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') 
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
        print ('zip completed')
    z.close()
zip_ya('./My_Call_For_Code_Pro-master','./My_Call_For_Code_Pro-master.zip')

metadata = {
    client.repository.DefinitionMetaNames.NAME              : "python-client-tutorial_training-definition",
    client.repository.DefinitionMetaNames.AUTHOR_EMAIL      : "wk821917@163com",
    client.repository.DefinitionMetaNames.FRAMEWORK_NAME    : "tensorflow",
    client.repository.DefinitionMetaNames.FRAMEWORK_VERSION : "1.5",
    client.repository.DefinitionMetaNames.RUNTIME_NAME      : "python",
    client.repository.DefinitionMetaNames.RUNTIME_VERSION   : "3.5",
    client.repository.DefinitionMetaNames.EXECUTION_COMMAND : "python3 My_Call_For_Code_Pro-master/lstm_pred_pro.py"
}

definition_details = client.repository.store_definition( "My_Call_For_Code_Pro-master.zip", meta_props=metadata )
definition_uid     = client.repository.get_definition_uid( definition_details )
print( "definition_uid: ", definition_uid )

metadata = {
client.training.ConfigurationMetaNames.NAME         : "python-client-tutorial_training-run",
client.training.ConfigurationMetaNames.AUTHOR_EMAIL : "wk281917@163.com",
client.training.ConfigurationMetaNames.TRAINING_DATA_REFERENCE : {
   "connection" : { 
      "endpoint_url"          : "https://s3-api.us-geo.objectstorage.softlayer.net",
      "aws_access_key_id"     : "f1ac76f0074244f9a07d5debb286f122",
      "aws_secret_access_key" : "c623bb131af41897c674eec7f7700446fdbeecf6c993d105"
      },
   "source" : { 
      "bucket" : "wktest2",
      },
      "type" : "s3"
   },
client.training.ConfigurationMetaNames.TRAINING_RESULTS_REFERENCE: {
   "connection" : {
      "endpoint_url"          : "https://s3-api.us-geo.objectstorage.softlayer.net",
      "aws_access_key_id"     : "f1ac76f0074244f9a07d5debb286f122",
      "aws_secret_access_key" : "c623bb131af41897c674eec7f7700446fdbeecf6c993d105"
      },
      "target" : {
         "bucket" : "predict",
      },
      "type" : "s3"
   }
}

print('------------submit and run------------')
run_details = client.training.run( definition_uid, meta_props=metadata )
run_uid     = client.training.get_run_uid( run_details )
print( "run_uid: ", run_uid )

while not(client.training.get_status( run_uid )['state']=='completed'):
    print(client.training.get_status( run_uid ))
    if client.training.get_status( run_uid )['state']=='error':
        error_flag = True
        break
    time.sleep(10)

if error_flag:
    print('--------something wrong during training ,see the log with training_id in the cos--------')
else:
    print('------------run over------------')

    if not os.path.exists('./history'): os.mkdir('./history')

    print('------------download file from COS------------')
    name = 'predict'
    bucket_obj = cos.Bucket(name)

    current_time = str(int(time.time()))
    bucket_obj.download_file(run_uid+'/predict_result/result.csv', './history/result'+current_time+'.csv')

    bucket_obj.download_file(run_uid+'/predict_result/input_data.csv', './history/input_data'+current_time+'.csv')


    bucket_obj.download_file(run_uid+'/last_time/last_time.json', './last_time.json')


    print('------------upload to the COS------------')
    name = 'history'
    bucket_obj = cos.Bucket(name)
    bucket_obj.upload_file('./history/result'+current_time+'.csv', 'result'+current_time+'.csv')

    bucket_obj.upload_file('./history/input_data'+current_time+'.csv', 'input_data'+current_time+'.csv')

    os.remove('./history/input_data'+current_time+'.csv')
    os.remove('./history/result'+current_time+'.csv')

