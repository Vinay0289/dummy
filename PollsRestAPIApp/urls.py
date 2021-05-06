from django.urls import path
from .views import ListUser,DetailUser,ListCategory,DetailCategory,ListSubCategory,DetailSubCategory,ListPoll,DetailPoll,ListPollOption,DetailPollOption,ListPollResult,DetailPollResult

urlpatterns = [
    path('users', ListUser.as_view(), name='users'),
    path('users/<int:pk>/', DetailUser.as_view(), name='detailuser'),
    path('categories',ListCategory.as_view(), name='categories'),
    path('categories/<int:pk>/',DetailCategory.as_view(), name='detailscategories'),
    path('subcategories',ListSubCategory.as_view(), name='subcategories'),
    path('subcategories/<int:pk>/',DetailSubCategory.as_view(), name='detailssubcategories'),
    path('poll',ListPoll.as_view(), name='poll'),
    path('poll/<int:pk>/',DetailPoll.as_view(), name='detailspoll'),
    path('polloption',ListPollOption.as_view(), name='polloption'),
    path('polloption/<int:pk>/',DetailPollOption.as_view(), name='detailspolloption'),
    path('pollresult',ListPollResult.as_view(), name='pollresult'),
    path('pollresult/<int:pk>/',DetailPollResult.as_view(), name='detailspollresult'),
]
