import requests
import os
import zipfile


data_dir = 'data'
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

annotation_url = 'http://mmlab.ie.cuhk.edu.hk/projects/WIDERFace/support/bbx_annotation/wider_face_split.zip'
annotation_zip_file="wider_face_split.zip"
#Train data
image_zip_file_train = 'WIDER_train.zip'
file_id_train = '0B6eKvaijfFUDQUUwd21EckhUbWs'
destination_train = 'data/WIDER_train.zip'

#Val data
image_zip_file_val = 'WIDER_val.zip'
file_id_val = '0B6eKvaijfFUDd3dIRmpvSk8tLUk'
destination_val = 'wider_data/WIDER_val.zip'



def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def download_file_from_web_server(url, destination):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    response = requests.get(url, stream=True)
    save_response_content(response, os.path.join(destination, local_filename))

    return local_filename


#  TODO Add progress bar
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def extract_zip_file(zip_file_name, destination):
    zip_ref = zipfile.ZipFile(zip_file_name, 'r')
    zip_ref.extractall(destination)
    zip_ref.close()


def download_widerface(train=True,val=True,annotation=True,data_dir=data_dir,
            file_id_train=file_id_train,destination_train=destination_train,image_zip_file_train=image_zip_file_train,
            file_id_val=file_id_val,destination_val=destination_val,image_zip_file_val=image_zip_file_val):

    if train:
        print('downloading the train images from google drive...')
        download_file_from_google_drive(file_id_train, destination_train)
        extract_zip_file(os.path.join(data_dir, image_zip_file_train), data_dir)
        os.remove(os.path.join(data_dir,image_zip_file_train))
        
        
    if val:
        print('downloading the val images from google drive...')
        download_file_from_google_drive(file_id_val, destination_val)
        extract_zip_file(os.path.join(data_dir, image_zip_file_val), data_dir)
        os.remove(os.path.join(data_dir,image_zip_file_val))
        
    if annotation:
        print('downloading the bounding boxes annotations...')
        annotation_zip_file = download_file_from_web_server(annotation_url,data_dir)
        extract_zip_file(os.path.join(data_dir,"wider_face_split.zip"), data_dir)
        os.remove(os.path.join(data_dir,annotation_zip_file))
        
    print("done !")
if __name__ == "__main__":
    

    download_widerface(train=True,val=True)

    
