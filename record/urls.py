from django.urls import path
from . import views

app_name='record'
urlpatterns = [
    #path('record/list/', views.RecordListView.as_view(), name='record_list'),
    path('', views.RecordListView.as_view(), name='record_list'),
    path('record/<int:pk>/', views.RecordDetailView.as_view(), name='record_detail'),
    
    #path('record/create/', views.RecordCreateView.as_view(), name='record_create'),
    path('record/create/', views.record_create, name='record_create'),
    
    #path('record/update/<int:pk>/', views.RecordUpdateView.as_view(), name='record_update'),
    path('record/<int:pk>/update/', views.record_update, name='record_update'),
    
    path('record/delete/<int:pk>/', views.RecordDeleteView.as_view(), name='record_delete'),
    #path('record/delete/<int:pk>/', views.record_delete, name='record_delete'),
    
    path('record/article/', views.RecordArticleView.as_view(), name='record_article'),
    path('record/python/', views.RecordPythonView.as_view(), name='record_python'),
    path('record/server/', views.RecordServerView.as_view(), name='record_server'),   
]