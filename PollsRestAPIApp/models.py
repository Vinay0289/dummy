from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    #parent=models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    Title=models.CharField(max_length=50)
    Keywords=models.CharField(max_length=255)
    Description=models.CharField(max_length=255)
    slug=models.SlugField()
    IsActive=models.BooleanField(default=True)
    CreatedDate=models.DateTimeField(auto_now_add=True)
    ModifiedDate=models.DateTimeField(auto_now=True )
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.Title


class SubCategory(models.Model):
    #parent=models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    Category = models.ForeignKey(Category,on_delete=models.CASCADE)
    Title=models.CharField(max_length=50)
    Keywords=models.CharField(max_length=255)
    Description=models.CharField(max_length=255)
    slug=models.SlugField()
    IsActive=models.BooleanField(default=True)
    CreatedDate=models.DateTimeField(auto_now_add=True)
    ModifiedDate=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'SubCategories'
    def __str__(self):
        return self.Title


class Poll(models.Model):
    Category = models.ForeignKey(Category,on_delete=models.CASCADE)
    SubCategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=255)
    slug=models.SlugField()
    TargetedIndustry = models.TextField(null=True,blank=True)
    QuestionPointingTo = models.TextField(null=True,blank=True)
    isMultipleType=models.BooleanField(default=False)
    isActive=models.BooleanField(default=True)
    createdDate=models.DateTimeField(auto_now_add=True)
    modifiedDate=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PollOption(models.Model):
    Poll = models.ForeignKey(Poll, related_name='polloptions', on_delete=models.CASCADE)
    optionDescription=models.CharField(max_length=100)
    isActive=models.BooleanField(default=True)
    createdDate=models.DateTimeField(auto_now_add=True)
    modifiedDate=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.optionDescription



class PollResult(models.Model):
    poll = models.ForeignKey(Poll, related_name='poll', on_delete=models.CASCADE)
    polloptions = models.ForeignKey(PollOption, related_name='polloptions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    otherDescription =models.CharField(max_length=255,blank=True,null=True)
    polldatetime =models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id)
