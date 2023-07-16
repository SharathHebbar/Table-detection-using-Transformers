import os
import shutil
from pathlib import Path, PurePath

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form, HTTPException
from dotenv import load_dotenv

from folder_creation import make_directory_if_not_exists
from pdf_to_img import pdf_to_image
from table_extraction import Table_extraction
from minio_services import MINIO

load_dotenv()

IMAGES_DIR = os.getenv('IMAGES_DIR')
PDF_DIR = os.getenv('PDF_DIR')
OUTPUTS_DIR = os.getenv('OUTPUTS_DIR')
HOST = os.getenv('HOST')
ACCESS_KEY = os.getenv('ACCESS_KEY')
MINIO_KEY = os.getenv('MINIO_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def main(file_name: str = Form(None), uid: str = Form(None)):
    try:
        make_directory_if_not_exists(IMAGES_DIR)
        IMAGES_DIR1 = IMAGES_DIR + uid + '/'
        make_directory_if_not_exists(IMAGES_DIR1)

        make_directory_if_not_exists(OUTPUTS_DIR)
        OUTPUTS_DIR1 = OUTPUTS_DIR + uid + '/'
        make_directory_if_not_exists(OUTPUTS_DIR1)
        print(file_name)
        if PurePath(file_name).suffix == '.pdf':
            imagename = pdf_to_image(file_name, IMAGES_DIR1)
        else:
            imagename = IMAGES_DIR1+Path(file_name).name
            shutil.copy(file_name, imagename)
            
        model = Table_extraction(imagename, OUTPUTS_DIR1)
        op_img = model.get_results()

        minio = MINIO(HOST, ACCESS_KEY, MINIO_KEY, BUCKET_NAME, uid, op_img)
        minio.upload_to_minio()
        obj = minio.download_from_minio()
        shutil.rmtree(IMAGES_DIR)
        shutil.rmtree(OUTPUTS_DIR)
        return obj

    except Exception as e:
        shutil.rmtree(IMAGES_DIR)
        shutil.rmtree(OUTPUTS_DIR)
        raise HTTPException(status_code=404, detail=str(e))
