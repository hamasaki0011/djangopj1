from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .models import Location,Sensors,Result
from .forms import LocationForm,SensorsForm
# ページへのアクセスをログインユーザーのみに制限する
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
import datetime

# from django.http import Http404
# from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponseRedirect
# from .application import data_rw
# for CSV file uploading
# import csv, io, datetime
# from django.http import HttpResponse 
# from sensor.forms import FileUploadForm
# import numpy as np
# from sensor import addCsv, writeCsv
# embeded watchdog module
# import sys
# import time
# from watchdog.observers import Observer
# from watchdog.events import RegexMatchingEventHandler
# from watchdog.events import LoggingEventHandler

import os
import logging
from main import addCsv
from .forms import FileUploadForm
# from .forms import UploadFileForm

# directory to store the uploading files
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'static/uploads/')
# Define debug log-file
logger = logging.getLogger('development')

class OwnerOnly(UserPassesTestMixin):
    def test_func(self):
        location_instance = self.get_object()
        return location_instance.user == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request,"You can edit and delete only for your's.")
        return redirect("main:location_detail", pk=self.kwargs["pk"])
# -----------------------------------------------------------------
# Top view, you can select a target site for remote monitoring
class IndexView(generic.ListView):
    template_name='main/main_index.html'
    model=Location
    # 2023.2.28　メモ
    # ユーザー情報を取得して、そのキーでフィルターをかける
    # クエリー取得を書く
# -----------------------------------------------------------------
# Main detail view, List view for sensor devices at each site 
class MainDetailView(generic.ListView):
    template_name='main/main_detail.html'
    model=Result

    def get(self, request, *args, **kwargs):
        # Get 'pk' which indicates the monitoring site information
        id=Location.objects.get(pk=self.kwargs['pk'])
        # Get the name of monitoring site
        location=Location.objects.get(pk=id.pk)
        # Get queryset for Measured_data, result
        # 注意：最終的にはtimedeltaで1分前のデータを表示するように調整する
        # Generate the table data including the device name and the most recent measured_data
        recent_update=datetime.date(2023,3,1)
        today = datetime.datetime.now()
        results=Result.objects.all().filter(place_id=id.pk, measured_date__range=(recent_update, today))
        
        # Prepare the data for chart drawing
        latest=30   # 30 minutes
        # if devive number is required it is defined by numDevice
        numDevice=15
        xdata=[]
        n=latest
        while(n>=0):
            xdata.append(-n)
            n-=1
        # Create y_Axis_data
        y_tmp=[[] for j in range(latest)]
        """ this means followings; 
            device0 : y_tmp[0][0] ~ y_tmp[0][29]
            device1 : y_tmp[1][0] ~ y_tmp[1][29]
            ...
            device5 : y_tmp[5][0] ~ y_tmp[1][29]
        """
        # define ydata lists with initializing
        ydata=[[] for j in range(latest)]        
        data_list=Result.objects.all().filter(place_id=id.pk) 
        # Get sensor device point's number
        sensor_list=Sensors.objects.filter(site_id=id.pk)
        # Get the number of sensor device point's 
        pointNum=len(sensor_list)
        # Get the smallest number of the point_id
        startPoint=sensor_list.order_by('id').first().id
        # Generate a graph data from sensor's measured_value
        for i in range(pointNum):
            # 課題：センサー番号がシリーズであることが前提のquery設定
            y_tmp[startPoint-1+i]=data_list.filter(point_id=startPoint+i).order_by('measured_date')[:latest]

            for data in y_tmp[startPoint-1+i]:
                ydata[startPoint-1+i].append(data.measured_value)
                
        # date=results.first().measured_date.strftime('%Y年%m月%d日')
        """
        'if' and 'for' Statements both do not form scopes in Python. 
        Therefore, the variable if inside the sentence is the same as the variable outside.
        Variables, 'start_at' and 'd_tmp' lator appeared are effective both inside and outside.
        """
        context={
            "pk":id.pk,
            "k":pointNum,
            "l":startPoint,

            # For the latest measured value table 
            "location":location,
            "results":results,
            "sensor_list":sensor_list,

            # For chart drawing
            "x_data":xdata,
            "ydata0":ydata[startPoint-1],
            "ydata1":ydata[startPoint],
            "ydata2":ydata[startPoint+1],
            "ydata3":ydata[startPoint+2],
            "ydata":ydata, 
        }
        
        return render(request, "main/main_detail.html", context)
# -----------------------------------------------------------------
# Locations' list view 
class LocationListView(generic.ListView):
    template_name='main/location_list.html'
    model=Location
    
    def get_queryset(self):
        qs = Location.objects.all()
        # ユーザーがログインしていれば、リストを表示する
        # q = self.request.GET.get("search")
        # qs = Record.objects.search(query=q)
        # if self.request.user.is_authenticated:
        #     qs = qs.filter(Q(public=True)|Q(user=self.request.user))
        # else:
        #     qs = qs.filter(public=True)
        # the selected records are re-ordered  by "created_date"         
        qs = qs.order_by("created_date")[:7]
        return qs
# -----------------------------------------------------------------
# Each location's detail information view
class LocationDetailView(generic.DetailView):
    template_name='main/location_detail.html'
    model=Location
    
    # def get_object(self):
    #     return super().get_object()
# -----------------------------------------------------------------
# Create a new location's information view
class LocationCreateModelFormView(LoginRequiredMixin,generic.CreateView):
    template_name = "main/location_form.html"
    form_class = LocationForm
    success_url = reverse_lazy("main:location_list")
    
    # user情報を取得する
    def get_form_kwargs(self):
        kwgs=super().get_form_kwargs()
        kwgs["user"]=self.request.user
        return kwgs
    
    # このviewではデータの取り込み、保存も一括して行われるので以下はいらない。  
    # # Received and saved data 
    # def form_valid(self, form):
    #     data = form.cleaned_data    # 入力したデータを辞書型で取り出す
    #     obj=Location(**data)        # 入力したデータでオブジェクトを作成し保存する
    #     obj.save()
    #     return super().form_valid(form)
"""
Another way to create
class LocationCreateView(LoginRequiredMixin,generic.CreateView):
    template_name='main/location_create.html'
    # model=Location
    form_class=LocationForm
    success_url=reverse_lazy('main:location_list')
    
    # Received and saved data 
    def form_valid(self, form):
        location = form.save(commit=False)
        # location.author = self.request.user
        location.crteated_date = timezone.now()
        location.updated_date = timezone.now()
        location.save()
        return super().form_valid(form)
"""
# -----------------------------------------------------------------
# Update location's information
class LocationUpdateModelFormView(OwnerOnly,generic.UpdateView):
    template_name = "main/location_form.html"
    form_class = LocationForm
    success_url = reverse_lazy("main:location_list")
    # Following get_querryset() is mondatly requrered.
    # in case of using a FormView
    def get_queryset(self):
        qs = Location.objects.all()
        return qs
    # Update updated_date
    def form_valid(self, form):
        location = form.save(commit=False)
        location.updated_date = timezone.now()
        location.save()
        return super().form_valid(form)
"""
Another way
class LocationUpdateView(LoginRequiredMixin,generic.UpdateView):
class LocationUpdateView(generic.UpdateView):
    template_name = 'main/location_update.html'
    model = Location
    # form_class = LocationForm
    fields = ('name', 'memo',)
    success_url = reverse_lazy('main:location_list')
 
    def form_valid(self, form):
        location = form.save(commit=False)
        # location.author = self.request.user
        location.updated_date = timezone.now()
        location.save()
        return super().form_valid(form)
"""
# -----------------------------------------------------------------
# Delete location information
class LocationDeleteView(OwnerOnly,generic.DeleteView):
    template_name = 'main/location_delete.html'
    model = Location
    # form_class=LocationForm
    success_url = reverse_lazy('main:location_list')
# -----------------------------------------------------------------
# Sensors' list view 
class SensorsListView(generic.ListView):
    template_name='main/sensor_list.html'
    model=Sensors

    # user情報を取得する
    def get_form_kwargs(self):
        kwgs=super().get_form_kwargs()
        kwgs["user"]=self.request.user
        return kwgs
    
    # def get_queryset(self):
    #     qs = Sensors.objects.all()
    #     # ユーザーがログインしていれば、リストを表示する
    #     # q = self.request.GET.get("search")
    #     # qs = Record.objects.search(query=q)
    #     # if self.request.user.is_authenticated:
    #     #     qs = qs.filter(Q(public=True)|Q(user=self.request.user))
    #     # else:
    #     #     qs = qs.filter(public=True)
    #     # # the selected records are re-ordered  by "created_date"         
    #     # qs = qs.order_by("created_date")[:7]
    #     return qs
# -----------------------------------------------------------------
# Each Sensors's detail information view
class SensorsDetailView(generic.DetailView):
    template_name='main/sensors_detail.html'
    model=Sensors
# class SensorDeviceDetailView(generic.DetailView):
#     def get(self,request, *args,**kwargs):
#         id=SensorDevice.objects.get(pk=self.kwargs['pk'])
#         site=SensorDevice.objects.get(id=id.pk)
#         data=MeasureData.objects.filter(point_id=id.pk)
#         # # as following if you use "filter", you can get all contents of DB
#         # memo=SensorDevice.objects.get(pk=sensor_device_id) 
#         context={
#             "id":id,
#             "site":site,
#             "data":data
#         }
#         return render(request, 'sensor/detail.html', context)
#     #  model=SensorDevice
#     #  template_name= 'sensor/detail.html'    

# # class SensorDeviceDetailView(generic.DetailView):
# #     template_name='sensor/sensor_device_detail.html'
# #     model=SensorDevice
# -----------------------------------------------------------------
# Create a new Sensor place information view
class SensorsCreateModelFormView(generic.CreateView):
    template_name = "main/sensors_create.html"
    form_class = SensorsForm
    success_url = reverse_lazy("main:sensors_list")
    
    # place情報を取得する
    # def get_form_kwargs(self):
    #     kwgs=super().get_form_kwargs()
    #     kwgs["place"]=self.place
    #     return kwgs
    
    # このviewではデータの取り込み、保存も一括して行われるので以下はいらない。  
    # # Received and saved data 
    # def form_valid(self, form):
    #     data = form.cleaned_data    # 入力したデータを辞書型で取り出す
    #     obj=Location(**data)        # 入力したデータでオブジェクトを作成し保存する
    #     obj.save()
    #     return super().form_valid(form)
"""Another way to create
# class SensorsCreateView(LoginRequiredMixin,generic.CreateView):
class SensorsCreateView(generic.CreateView):
    template_name='main/sensors_create.html'
    model=Sensors
    # form_class=LocationForm
    success_url=reverse_lazy('main:sensors_list')
    
    # Received and saved data 
    def form_valid(self, form):
        sensors = form.save(commit=False)
        # sensors.author = self.request.user
        sensors.crteated_date = timezone.now()
        sensors.updated_date = timezone.now()
        sensors.save()
        return super().form_valid(form)
"""
# -----------------------------------------------------------------
# Update location's information
class SensorsUpdateModelFormView(generic.UpdateView):
    template_name = "main/sensors_update.html"
    form_class = SensorsForm
    success_url = reverse_lazy("main:sensors_list")
    
    # Following get_querryset() is mondatly requrered.
    # in order to get place data
    def get_queryset(self):
        return Sensors.objects.all()
    # Update updated_date
    def form_valid(self, form):
        sensors = form.save(commit=False)
        sensors.updated_date = timezone.now()
        sensors.save()
        return super().form_valid(form)
"""
Another way
class LocationUpdateView(LoginRequiredMixin,generic.UpdateView):
class LocationUpdateView(generic.UpdateView):
    template_name = 'main/location_update.html'
    model = Location
    # form_class = LocationForm
    fields = ('name', 'memo',)
    success_url = reverse_lazy('main:location_list')
 
    def form_valid(self, form):
        location = form.save(commit=False)
        # location.author = self.request.user
        location.updated_date = timezone.now()
        location.save()
        return super().form_valid(form)
"""
# -----------------------------------------------------------------
# Delete Sensor information
class SensorsDeleteView(generic.DeleteView):
    template_name = 'main/sensors_delete.html'
    model = Sensors
    # form_class=LocationForm
    success_url = reverse_lazy('main:sensors_list')
# -----------------------------------------------------------------
# 2022/11/8 CSV file uplaoding
# it does need as reverse url path, does not it need? at 2022/11/11  
# def index(req):
#     return render(req, 'main/index.html')

# class DetailView(generic.DetailView):
#     def get(self,request, *args,**kwargs):
#         # in this case, "pk" indicates the point_id
#         id=SensorDevice.objects.get(pk=self.kwargs['pk'])
#         site=SensorDevice.objects.get(id=id.pk)
#         data=MeasureData.objects.filter(point_id=id.pk)
#         # # as following if you use "filter", you can get all contents of DB
#         # memo=SensorDevice.objects.get(pk=sensor_device_id) 
#         context={
#             "id":id,
#             "site":site,
#             "data":data
#         }
#         return render(request, 'sensor/detail.html', context)
#     #  model=SensorDevice
#     #  template_name= 'sensor/detail.html'

# def detail(request, sensor_device_id):
#     device=get_object_or_404(SensorDevice, pk=sensor_device_id)
#     # # as following if you use "filter", you can get all contents of DB
#     # memo=SensorDevice.objects.get(pk=sensor_device_id) 
#     context={
#         "device":device,
#     }
#     return render(request, 'sensor/detail.html', context)
#     # try:
#     #     device = SensorDevice.objects.get(pk=sensor_device_id)
#     # except SensorDevice.DoesNotExist:
#     #     raise Http404("SensorDevice does not exist")
#     # return render(request, 'sensor/detail.html', {'device': device })
# -----------------------------------------------------------------
# hundling the uploading file
def handle_uploaded_file(f):
    path = os.path.join(UPLOAD_DIR, f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    try:
        addCsv.insert_csv_data(path)        # register the contents of csv file' to DB
        # writeCsv.insert_csv_data(path)    # register the csv file' data to DB
    except Exception as exc:
        logger.error(exc)
    # Delete the apploading completed file
    os.remove(path)                         
# -----------------------------------------------------------------
# CSV file uploading
class Upload(generic.FormView):
    template_name = 'main/upload.html'
    form_class = FileUploadForm
    
    def get_form_kwargs(self):
        # set prefix of correct csv file's name into valiables
        valiables='test'    # valiable to pass to form
        kwargs=super(Upload,self).get_form_kwargs()
        kwargs.update({'valiables':valiables})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context = {
            'form': form,
        }
        return context

    def form_valid(self, form):
        handle_uploaded_file(self.request.FILES['file'])
        return redirect('main:upload_complete')  # to redirect to upload complete view
"""
Another way
def upload(request):
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return redirect('main:upload_complete')  # アップロード完了画面にリダイレクト
    else:
        # form = UploadFileForm()
        form = FileUploadForm()
    return render(request, 'main/upload.html', {'form': form})
"""
# -----------------------------------------------------------------
# Complete the file uploading
class UploadComplete(generic.FormView):
    template_name = 'main/upload_complete.html'
    form_class = FileUploadForm
"""
Another way
def upload_complete(request):
    return render(request, 'main/upload_complete.html')
    return render(request, 'main/upload.html')
"""
# -----------------------------------------------------------------
# class Load(generic.FormView):
#     template_name = 'load.html'
#     form_class = FileUploadForm
    
#     def get_form_kwargs(self):
#         # set prefix of correct csv file's name into valiables
#         valiables='test'    # valiable to pass to form
#         kwargs=super(Load,self).get_form_kwargs()
#         kwargs.update({'valiables':valiables})
#         return kwargs

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         form = self.get_form()
#         context = {
#             'form': form,
#         }
#         return context

#     def form_valid(self, form):
#         handle_uploaded_file(self.request.FILES['file'])
#         # return redirect('sensor:upload_complete')  # to redirect to upload complete view
#         return redirect('sensor:load')
#         # 2022.12.21 why can not return to index page from here
#         # return redirect('index(req)')

# 2022/12/21 Download csv file 
# def download(request):
#     # To produce csv file to download
#     response = HttpResponse(content_type='text/csv')
#     # 2022/12/21 need to generate a "filename" based on the download data
#     response['Content-Disposition'] = 'attachment;  filename="VerticalWriting_FUJICO.csv"'
#     writer = csv.writer(response)
#     # 2022/12/21 arrange csv format data
#     writer.writerow(['F','as 1st letter'])
#     writer.writerow(['U','as 2nd letter'])
#     writer.writerow(['J','as 3rd letter'])
#     writer.writerow(['C','as 4th letter'])
#     writer.writerow(['O','as 5th letter'])
#     return response

# def call_write_data(req):
#     if req.method == 'GET':
#         # write_data.pyのwrite_csv()メソッドを呼び出す。
#         # ajaxで送信したデータのうち"input_data"を指定して取得する。
#         data_rw.write_csv_1(req.GET.get("input_data"))
#         data_rw.write_csv_1(req.GET.get("input_data1"))
#         # 読み出し、write_data.pyの中に新たに記述したメソッド(return_text())を呼び出す。
#         data = data_rw.return_text(req.GET.get("input_data"))
#         data1 = data_rw.return_text(req.GET.get("input_data1"))
#         # 受け取ったデータをhtmlに渡す。
#         return HttpResponse(data)
#         # writeの場合のリターン
#         #return HttpResponse()
