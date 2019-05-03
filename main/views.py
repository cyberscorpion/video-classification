from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
import os
import numpy as np
import cv2
import time
import tensorflow as tf
from keras.models import model_from_json

from .models import *

from django.core.files.storage import FileSystemStorage

project_path = "/home/rajat/workspace/activity/sample_project/"

class Videoto3D:

    def __init__(self,n_channels, width, height, depth,n_videos):
        self.width = width
        self.height = height
        self.depth = depth
        self.n_channels=n_channels
        self.n_videos=n_videos
    
    def video3d(self, filename, color=False, skip=True):
        #filename of the corresponding video
        
        cap = cv2.VideoCapture(project_path+"media/"+filename)        
        
        nframe = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        
        if skip:
            frames = [x * nframe / self.depth for x in range(1,(self.depth+1))]
        else:
            frames = [x for x in range(self.depth)]
        
        
        frames=frames[(int(len(frames)/2)-5):(int(len(frames)/2)+5)]
        
        framearray = []

        for i in range(len(frames)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frames[i])
            ret, frame = cap.read()
            frame = cv2.resize(frame, (self.height, self.width))
            #img = cv2.imread('messi5.jpg',0)
            #frame = cv2.Canny(frame,224,224)
            #if color:
            #framearray.append(frame)
              
            #else:
            
            frame=cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            framearray.append(cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB))
               
        cap.release()
        
        
        
        return np.array(framearray)
    
def func(filename):
    vid3d = Videoto3D(3,224, 224, 30,1)
    #vid3d = Videoto3D(3,128, 128, 60,300)
    X_predict=[]
    X_predict.append(vid3d.video3d(filename))
    X_predict=np.array(X_predict)
    #print(X_predict)
    json_file = open(project_path+'model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(project_path+"model.h5")
    print("Loaded model from disk")
    Y_pred=loaded_model.predict(X_predict)
    print(Y_pred)
    final_result =1 
    return 1
#    return Y_predict
    

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            file_object = File.objects.all().order_by('-timestamp')
            file_object = file_object.first()
            fs = FileSystemStorage()
            filename = fs.save('rajat.mp4', file_object.file)
            result = func(file_object.filename())
            return Response({'result': result})
        else:
            return Response(file_serializer.errors, staticmethodtus=status.HTTP_400_BAD_REQUEST)