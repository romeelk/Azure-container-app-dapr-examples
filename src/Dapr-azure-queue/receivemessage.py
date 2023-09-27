from flask import Flask, request
import time
import os
import requests
import base64
from PIL import Image
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


daprPort = os.getenv('DAPR_HTTP_PORT')
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
app = Flask(__name__)
@app.route("/processmessage", methods=['POST'])
def incoming():
    #print(request.data.decode('UTF-8'), flush=True)
    file = request.data.decode('UTF-8')
    
    thumbnail_file = resize(file)
    upload_file(thumbnail_file)
    return "Message processed"

def resize(file):

    local_path = "./images"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    print(f"\n Fetching image to resize from blob container images {file} ", flush=True)

    container_client = blob_service_client.get_container_client(container="images") 
    download_file_path = os.path.join(local_path,file)

    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(file).readall())

    #Upload the created file
    with Image.open(download_file_path) as image:
        image.load()

    print(image.size, flush=True)
    image.thumbnail((90,90))
    thumbnail_file = os.path.join(local_path,f"thunb-{file}")
    image.save(thumbnail_file)

    return thumbnail_file

def upload_file(file):
    # Upload the thumbnail file
    print(file, flush=True)      
    
    ## read as binary
    with open(file=file, mode="rb") as filedata:
        binary_data = filedata.read()
    
    url = f'http://localhost:{daprPort}/v1.0/bindings/azureblob'
    # encode into base64 bytes
    base64_encoded_data = base64.b64encode(binary_data)
    # decode into base64 string
    base64_message = base64_encoded_data.decode('utf-8')
    uploadcontents = '{ "operation": "create", "data": "'+ base64_message+ '", "metadata": { "blobName": "'+ file+'" } }'
    requests.post(url, data = uploadcontents)
    print("uploaded file", flush=True)
           