import shutil
import base64
import cv2
import numpy as np
from fastapi import FastAPI, File,UploadFile
from rsa import sign_hash
from SignPredictor import  SignPredictor
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List



def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

app = FastAPI()


origins = [
    "http://localhost:3001",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sign_predictor = SignPredictor()




@app.post('/multi')
async def multi(file:UploadFile = File(...)):
    with open(f'temp_video.mp4','wb') as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    cap = cv2.VideoCapture("temp_video.mp4")
    output = sign_predictor.process_multisign(cap)

    
    return {"text":output}




@app.post('/single')
async def single(file:UploadFile = File(...)):
    with open(f'temp_video.mp4','wb') as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    cap = cv2.VideoCapture("temp_video.mp4")
    output = sign_predictor.process_sign(cap)

    
    return {"text":output}


class Data(BaseModel):
    data: List














@app.post("/test")
async def test(data:Data):
    frame_list_data = (data.data)
    frame_list = []
    for frame in frame_list_data:
        frame_list.append(readb64(frame)) 


    sign_id,sign_name = sign_predictor.predict(frame_list)
    return {"text":sign_name}





# uvicorn main:app --port 8001 --reload



# from SignPredictor import  SignPredictor
# import cv2
# from fastapi import FastAPI

# app = FastAPI()

# sign_predictor = SignPredictor()

# print("every thing initalized")


# @app.get('/')
# async def root():
#     cap = cv2.VideoCapture(0)
#     output = sign_predictor.process_multisign(cap)
#     print(output)
#     return {"message":output}



