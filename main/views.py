from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .models import Location,Sensors
from .forms import LocationForm,SensorsForm
# ページへのアクセスをログインユーザーのみに制限する
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone

# from django.http import Http404
# from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponseRedirect
# from .models import MeasureData, SensorDevice
# from .application import data_rw
# for CSV file uploading
# import csv, io, datetime
# from django.http import HttpResponse 
# from sensor.forms import FileUploadForm
# import os
# import numpy as np
# from sensor import addCsv, writeCsv
# import logging
# embeded watchdog module
# import sys
# import time
# from watchdog.observers import Observer
# from watchdog.events import RegexMatchingEventHandler
# from watchdog.events import LoggingEventHandler

# directory to store the uploading files
# UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../static/upload/')
# Define debug log-file
# logger = logging.getLogger('development')

class OwnerOnly(UserPassesTestMixin):
    def test_func(self):
        location_instance = self.get_object()
        return location_instance.user == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request,"You can edit and delete only for your's.")
        return redirect("main:location_detail", pk=self.kwargs["pk"])

# -----------------------------------------------------------------
# Top view, you can select a target site for remote monitoring
class IndexView(generic.TemplateView):
    template_name='main/main_index.html'
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
    # def get_form_kwargs(self):
    #     kwgs=super().get_form_kwargs()
    #     kwgs["user"]=self.request.user
    #     return kwgs
    
    # このviewではデータの取り込み、保存も一括して行われるので以下はいらない。  
    # # Received and saved data 
    # def form_valid(self, form):
    #     data = form.cleaned_data    # 入力したデータを辞書型で取り出す
    #     obj=Location(**data)        # 入力したデータでオブジェクトを作成し保存する
    #     obj.save()
    #     return super().form_valid(form)

# Another way to create
# class LocationCreateView(LoginRequiredMixin,generic.CreateView):
#     template_name='main/location_create.html'
#     # model=Location
#     form_class=LocationForm
#     success_url=reverse_lazy('main:location_list')
    
#     # Received and saved data 
#     def form_valid(self, form):
#         location = form.save(commit=False)
#         # location.author = self.request.user
#         location.crteated_date = timezone.now()
#         location.updated_date = timezone.now()
#         location.save()
#         return super().form_valid(form)

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

# Another way
# class LocationUpdateView(LoginRequiredMixin,generic.UpdateView):
# class LocationUpdateView(generic.UpdateView):
#     template_name = 'main/location_update.html'
#     model = Location
#     # form_class = LocationForm
#     fields = ('name', 'memo',)
#     success_url = reverse_lazy('main:location_list')
 
#     def form_valid(self, form):
#         location = form.save(commit=False)
#         # location.author = self.request.user
#         location.updated_date = timezone.now()
#         location.save()
#         return super().form_valid(form)
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
    # def get_form_kwargs(self):
    #     kwgs=super().get_form_kwargs()
    #     kwgs["user"]=self.request.user
    #     return kwgs
    
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
# Another way to create
# # class SensorsCreateView(LoginRequiredMixin,generic.CreateView):
# class SensorsCreateView(generic.CreateView):
#     template_name='main/sensors_create.html'
#     model=Sensors
#     # form_class=LocationForm
#     success_url=reverse_lazy('main:sensors_list')
    
#     # Received and saved data 
#     def form_valid(self, form):
#         sensors = form.save(commit=False)
#         # sensors.author = self.request.user
#         sensors.crteated_date = timezone.now()
#         sensors.updated_date = timezone.now()
#         sensors.save()
#         return super().form_valid(form)
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
# Another way
# class LocationUpdateView(LoginRequiredMixin,generic.UpdateView):
# class LocationUpdateView(generic.UpdateView):
#     template_name = 'main/location_update.html'
#     model = Location
#     # form_class = LocationForm
#     fields = ('name', 'memo',)
#     success_url = reverse_lazy('main:location_list')
 
#     def form_valid(self, form):
#         location = form.save(commit=False)
#         # location.author = self.request.user
#         location.updated_date = timezone.now()
#         location.save()
#         return super().form_valid(form)
# -----------------------------------------------------------------
# Delete Sensor information
class SensorsDeleteView(generic.DeleteView):
    template_name = 'main/sensors_delete.html'
    model = Sensors
    # form_class=LocationForm
    success_url = reverse_lazy('main:sensors_list')
# -----------------------------------------------------------------
# View of main list 
class MainListView(generic.ListView):
    template_name='main/main_list.html'
    model=Sensors
    
    # place情報を取得する
    # その前にA社(id=1)のデータのみ呼び出す。
     # in this case, "pk" indicates place_id
    def get_queryset(self):
        qs = Sensors.objects.all()
        id=1
        sensors_list=qs.filter(place_id=id)
        return sensors_list
        
        # user_obj = self.request.user
        # if user.is_authenticated:
        #     qs = Sensors.objects.all()
        #     id=1
        #     sensors_list=qs.filter(place_id=id)
        #     return sensors_list
        # else:
        #     qs = Sensors.objects.none()
        #     return qs

    # user情報を取得する
    # def get_form_kwargs(self):
    #     kwgs=super().get_form_kwargs()
    #     kwgs["user"]=self.user
    #     return kwgs

    # def get_queryset(self):
    #     # まずは、A社みのリストを表示する
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
# List view for sensor devices at each site
# class SensorDeviceListView(generic.ListView):
#     # template_name='sensor/sensor_device_list.html'
#     # model=MeasureData
#     # context_object_name = 'MeasureData_list'
#     # return render(request, 'sensor/detail.html', {'location': name})
#     def get(self, request, *args, **kwargs):
#         # in this case, "pk" indicates place_id
#         id=SensorDevice.objects.get(pk=self.kwargs['pk'])
#         location=Location.objects.get(pk=id.pk)
#         # set queryset to search "device" object in SensorDevice DB
#         sensor_list=SensorDevice.objects.filter(site=id.pk)
#         data_list=MeasureData.objects.filter(place=id.pk)
#         sensor = [] 
#         note = []
#         measuredata=[]
#         measured=[]
#         x_data=[]
#         ydata=[[] for i in range(12)]
#         latest=30   #the latest indicator

#         """
#         'if' and 'for' Statements both do not form scopes in Python. 
#         Therefore, the variable if inside the sentence is the same as the variable outside.
#         Variables, 'start_at' and 'd_tmp' lator appeared are effective both inside and outside.
#         """
#         # to set sonsor device'
#         if id.pk == 1:  start_at = 0
#         elif id.pk == 2:    start_at = 4
#         elif id.pk == 3:    start_at = 8
#         # we generate a get_id from "point_id"
#         for n in range(start_at, start_at + len(sensor_list)):
#             s_tmp = sensor_list.get(id = n + 1)
#             sensor.append(s_tmp)       
#             note.append(s_tmp.note)
#             # d_tmp = data_list.filter(point_id = n + 1).order_by('created_at').reverse().first()
#             temp = data_list.filter(point_id = n + 1).order_by('created_at')
#             last=len(temp)
#             tmp=temp[last-latest:last+1]
#             for data in tmp:
#                 ydata[n].append(data.data_value)
#                 # y_data.append(data.data_value)

#             d_tmp = temp.reverse().first()
#             measuredata.append(d_tmp.data_value)
#             measured.append(d_tmp.measured_at.strftime('%H:%M'))    #d_tmp.measured_at.strftime('%H:%M:%S')
#             # for data in tmp:
#             #     y_data.append(data.data_value)

#         if len(sensor_list) < 5:
#             for n in range(5-len(sensor_list)):
#                 sensor.append(" <- N/A -> ")
#                 note.append("  ")
#                 measuredata.append(" -- ")
#                 measured.append("  ")
#                 # Remark: 2022.12.16 What should I do make y_data list in case of no valid data

#         date=d_tmp.measured_at.strftime('%Y年%m月%d日')

#         # Prepare Xaxis data for 30 minutes data display
#         m=latest
#         while(m>=0):
#             x_data.append(-m)
#             m-=1

#         if(id.pk==1):
#             ydata0=ydata[0]
#             ydata1=ydata[1]
#             ydata2=ydata[2]
#             ydata3=ydata[3]
#         elif(id.pk==2):
#             ydata0=ydata[4]
#             ydata1=ydata[5]
#             ydata2=ydata[6]
#             ydata3=ydata[7]
#         else:
#             ydata0=ydata[8]
#             ydata1=ydata[9]
#             ydata2=ydata[10]
#             ydata3=ydata[11]

#         context={
#             "pk":id.pk,
#             # Not only for Table updating but also Chart drawing
#             "location":location,
#             "sensor_number":len(sensor_list),
#             "date":date,
#             "sensor0":sensor[0],
#             "sensor1":sensor[1],
#             "sensor2":sensor[2],
#             "sensor3":sensor[3],
#             "sensor4":sensor[4],
#             "note0":note[0],
#             "note1":note[1],
#             "note2":note[2],
#             "note3":note[3],
#             "note4":note[4],
#             # Only for Table updating
#             "data0":measuredata[0],
#             "data1":measuredata[1],
#             "data2":measuredata[2],
#             "data3":measuredata[3],
#             "data4":measuredata[4],
#             "date0":measured[0],
#             "date1":measured[1],
#             "date2":measured[2],
#             "date3":measured[3],
#             "date4":measured[4],
#             # only for chart drawing
#             "x_data":x_data,
#             # "y_data":y_data,
#             # "y_data0":y_data[0:13],     # 0 to 12 : 13
#             # "y_data1":y_data[13:26],    # 13 to 25 : 13 
#             # "y_data2":y_data[26:39],    # 
#             # "y_data3":y_data[39:52],
#             "ydata":ydata,
#             "ydata0":ydata0,
#             "ydata1":ydata1,
#             "ydata2":ydata2,
#             "ydata3":ydata3, 
#         }
#         return render(request, "sensor/sensor_device_list.html", context)

# 2022/11/8 CSV file uplaoding
# it does need as reverse url path, does not it need? at 2022/11/11  
# def index(req):
#     return render(req, 'main/index.html')

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

# class SensorListView(generic.ListView):
#     template_name='sensor/sensor_list.html'
#     model=SensorDevice

# # class SensorDeviceDetailView(generic.DetailView):
# #     template_name='sensor/sensor_device_detail.html'
# #     model=SensorDevice

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

# def results(request, location_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % location_id)

# def vote(request, location_id):
#     return HttpResponse("You're voting on question %s." % location_id)

# hundling the uploading file
# def handle_uploaded_file(f):
#     path = os.path.join(UPLOAD_DIR, f.name)
#     with open(path, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#     try:
#         # addCsv.insert_csv_data(path)    # register the csv file' data to DB
#         writeCsv.insert_csv_data(path)    # register the csv file' data to DB
#     except Exception as exc:
#         logger.error(exc)
#     os.remove(path) # delete the apploaded file

# file uploading trial_2 in case of using a class view at 2022/11/11
# class Upload(generic.FormView):
#     template_name = 'upload.html'
#     form_class = FileUploadForm
    
#     def get_form_kwargs(self):
#         # set prefix of correct csv file's name into valiables
#         valiables='test'    # valiable to pass to form
#         kwargs=super(Upload,self).get_form_kwargs()
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
#         return redirect('sensor:upload_complete')  # to redirect to upload complete view

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

# Complete view file uploading trial_2 at 2022/11/11
# class UploadComplete(generic.FormView):
#     template_name = 'upload_complete.html'
#     form_class = FileUploadForm

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

# class SensorSettingDoneView(generic.TemplateView):
#     template_name='sensor_setting_done.html'

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


