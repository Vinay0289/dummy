from rest_framework import serializers
from .models import Category,SubCategory,Poll,PollOption,PollResult
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=50, min_length=6)
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email already exists')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('username already exists')})

        return super().validate(args)
  

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email'
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'Title',
            'Keywords',
            'Description',
            'slug',
            'CreatedDate',
            'ModifiedDate'
        )
        model = Category

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'Category',
            'Title',
            'Keywords',
            'Description',
            'slug',
            'IsActive',
            'CreatedDate',
            'ModifiedDate'
        )
        model = SubCategory


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'Category',
            'SubCategory',
            'title',
            'description',
            'slug',
            'isMultipleType',
            'isActive',
            'createdDate',
            'modifiedDate'
        )
        model = Poll


class PollOptionSerializer(serializers.ModelSerializer):
#    Poll = serializers.ReadOnlyField(source='Poll.title',  read_only=False)

    class Meta:
        fields = (
            'id',
            'Poll',
            'optionDescription',
            'isActive',
            'createdDate',
            'modifiedDate'
        )
        model = PollOption



class PollResultSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'poll',
            'polloptions',
            'user',
            'otherDescription',
            'polldatetime'
        )
        model = PollResult