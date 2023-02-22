from django import forms
from .models import Location
# from .models import SensorDevice
# from .models import MeasureData
# import os
# import io, csv
# from django.core.exceptions import ValidationError
# VALID_EXTENSIONS=['.csv']

class LocationForm(forms.ModelForm):
    class Meta:
        model=Location
        # fields="__all__"
        # fields=('name','memo',)
        exclude=["user"]
    
    # viewで取得したuser情報を受け取る    
    def __init__(self,user=None, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs.update({"class":"form-control"})
        self.user=user
        super().__init__(*args, **kwargs)
    
    # 受け取ったuser情報を保存する
    def save(self,commit=True):
        location_obj=super().save(commit=False)
        if self.user:
            location_obj.user=self.user
        if commit:
            location_obj.save()
        return location_obj
        
class LocationFormClass(forms.Form):
    name = forms.CharField()
    memo = forms.CharField(widget=forms.Textarea())
 
    # def __init__(self, *args, **kwargs):
    #     for field in self.base_fields.values():
    #         field.widget.attrs.update({"class":"form-control"})
    #     super().__init__(*args, **kwargs)

# class SensorDeviceForm(forms.ModelForm):
#     class Meta:
#         model=SensorDevice
#         fields=(
#             'device', 'note',
#         )

# class MeasureDataForm(forms.ModelForm):
#     class Meta:
#         model=MeasureData
#         fields=(
#             'point', 'measured_at', 'data_value',
#         )

# # 2022/11/8 generate a button for CSV file uploading
# class FileUploadForm(forms.Form):  
#     file = forms.FileField(
#         label='アップロードするファイルを選択'
#     )

#     # receive the valiables which passed by views
#     def __init__(self, *args, **kwargs):
#         self.valiables=kwargs.pop('valiables',None) # get valiables
#         super(FileUploadForm, self).__init__(*args,**kwargs)

#     # Add file validation feature at 2022/11/11 
#     def clean_file(self):
#         file=self.cleaned_data['file']
#         extension=os.path.splitext(file.name)[1]    # get file' extension
#         # is it csv file or not?
#         if not extension.lower() in VALID_EXTENSIONS:
#             raise forms.ValidationError('csvファイルを選択して下さい')
#         # is it correct csv file or not?
#         if not file.name.startswith(self.valiables):
#             raise forms.ValidationError('間違った名前のcsvファイルです。''（'+ self.valiables + 'で始まるcsvファイルを選択してください。）')
