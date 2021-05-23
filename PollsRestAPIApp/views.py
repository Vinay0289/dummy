from django.shortcuts import render
from rest_framework import generics
from .models import Category,SubCategory,Poll,PollOption,PollResult
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer,UserSerializer,CategorySerializer,SubCategorySerializer,PollSerializer,PollOptionSerializer,PollResultSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import uuid
from django.http import HttpResponse
import json

# Create your views here.

class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        # serializer.is_valid(raise_exception = True)
        # serializer.save()
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                "RequestId": str(uuid.uuid4()),
                "Message": "User created successfully",
                
                "User": serializer.data}, status=status.HTTP_201_CREATED
                )
        
        return Response({"Errors": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)


class ListUser(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListCategory(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DetailCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ListSubCategory(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class DetailSubCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class ListPoll(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class DetailPoll(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Poll.objects.all()
    serializer_class = PollSerializer

class ListPollOption(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PollOption.objects.all()
    serializer_class = PollOptionSerializer

class DetailPollOption(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PollOption.objects.all()
    serializer_class = PollOptionSerializer


class ListPollResult(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PollResult.objects.all()
    serializer_class = PollResultSerializer

class DetailPollResult(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PollResult.objects.all()
    serializer_class = PollResultSerializer



def get_subcategory(request):
    id = request.GET.get('id', '')
    result = list(SubCategory.objects.filter(
    Category_id=int(id)).values('id', 'Title'))
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_PollOptions(request):
    id = request.GET.get('id', '')
    result = list(PollOption.objects.filter(
    Poll_id=int(id)).values('id', 'optionDescription'))
    return HttpResponse(json.dumps(result), content_type="application/json")

