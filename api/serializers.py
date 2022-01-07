from rest_framework import serializers
from .models import Task
from .models import File

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields ='__all__'
        
        
class FileSerializer(serializers.ModelSerializer):
	class Meta:
		model = File
		fields =('title','file')        