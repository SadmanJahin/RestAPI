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
import pickle
import librosa
# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls= {
        'List':'/task-list',
        'Detail View':'/task-detail/<str:pk>/',
        'Create':'/task-create',
        'Update':'/task-update',
        'Delete':'/task-delete',
        
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

def value(request):
    with open('model_pickle','rb') as file:
        mp = pickle.load(file)
        x=mp.predict([[5000]])
    return HttpResponse(x)
#def upload(request):
 #   if request.method=='POST':
#       title=request.POST['title']
 #      uploaded_file=request.FILES['file']
  #     fs=FileSystemStorage()
   #    name=fs.save(uploaded_file.name,uploaded_file)
    #   url=fs.url(name)
    #   return HttpResponse(url)
#    return HttpResponse("blank")




