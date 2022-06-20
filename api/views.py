from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .serializers import FileSerializer
from .models import Task
from .models import File
from django.core.files.storage import  FileSystemStorage
import librosa
import numpy as np
import pickle
from collections import Counter


# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls= {
        'List':'/audio-list',
        'Detail View':'/audio-detail/<str:pk>/',
        'Create':'/paitent-create',
        'Update':'/patient-update',
        'Delete':'/task-delete',
        'Get Heart Result':'/analyseHeartbeat',
    }
    return Response(api_urls)

@api_view(['GET'])
def taskList(request):
	tasks = Task.objects.all().order_by('-id')
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Task.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def taskUpdate(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	task.delete()

	return Response('Item succsesfully delete!')


@api_view(['POST'])
def upload(request):
	serializer = FileSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def analyseHeartbeat(request):
    
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
    name="media/documents/"+request.POST['title']
    data,sample_rate=librosa.load(name)
    mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=40).T,axis=0)

    scaler1= pickle.load(open("models/scaler(physionet).pkl", 'rb'))
    model1 = pickle.load(open("models/SVM(physionet).sav", 'rb'))
    model2 = pickle.load(open("models/RandomForest(Pascal).sav", 'rb'))
    model3 = pickle.load(open("models/KNN(Medical).sav", 'rb'))
    scaled_x1=scaler1.transform([mfccs])
    y_pred1 = model1.predict(scaled_x1)[0]
    if(y_pred1==-1):
        y_pred1="normal"
    else :
        y_pred1="abnormal"
     
    y_pred2 = str(model2.predict([mfccs])[0]).lower()
    y_pred3 = str(model3.predict([mfccs])[0]).lower()
    
    mode=Counter([y_pred1,y_pred2,y_pred3])
    
    hybrid_prediction=mode.most_common(1)[0][0]
    
    return HttpResponse(hybrid_prediction)
#def upload(request):
 #   if request.method=='POST':
#       title=request.POST['title']
 #      uploaded_file=request.FILES['file']
  #     fs=FileSystemStorage()
   #    name=fs.save(uploaded_file.name,uploaded_file)
    #   url=fs.url(name)
    #   return HttpResponse(url)
#    return HttpResponse("blank")

@api_view(['POST'])
def upload(request):
    
    if request.method=='POST':
        uploaded_file=request.FILES['bill']
        fs=FileSystemStorage()
        name=fs.save(uploaded_file.name,uploaded_file)
        
        
        
    location="media/"+name    
    data,sample_rate=librosa.load(location)
    #mfccs = librosa.feature.mfcc(y=data, sr=sr)
    #mfccs_scaled_feature=np.mean(mfccs.T,axis=0)
    scaler1= pickle.load(open("models/scaler(physionet).pkl", 'rb'))
    model1 = pickle.load(open("models/SVM(physionet).sav", 'rb'))
    model2 = pickle.load(open("models/RandomForest(Pascal).sav", 'rb'))
    model3 = pickle.load(open("models/KNN(Medical).sav", 'rb'))
    
    
    #data,sample_rate=librosa.load(serializer)
    mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=40).T,axis=0)
    scaled_x1=scaler1.transform([mfccs])
    y_pred1 = model1.predict(scaled_x1)[0]
    if(y_pred1==-1):
        y_pred1="normal"
    else :
        y_pred1="abnormal"
     
    y_pred2 = str(model2.predict([mfccs])[0]).lower()
    y_pred3 = str(model3.predict([mfccs])[0]).lower()
    
    mode=Counter([y_pred1,y_pred2,y_pred3])
    
    hybrid_prediction=mode.most_common(1)[0][0]
    
    return HttpResponse(hybrid_prediction)



