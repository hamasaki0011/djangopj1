from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Record
from .forms import RecordForm
from django.utils import timezone

class RecordListView(ListView):
    template_name='record/record_list.html'
    model=Record
    
class RecordDetailView(DetailView):
    template_name='record/record_detail.html'
    model=Record

def record_create(request):
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.author = request.user
            record.published_date = timezone.now()
            record.save()
            return redirect('record_detail', pk=record.pk)
    else:
        form = RecordForm()
    return render(request, 'record/record_create.html', {'form': form})

# class RecordCreateView(CreateView):
#     template_name='record_create.html'
#     form_class=RecordForm
#     success_url=reverse_lazy('record:record_create_complete')

def record_update(request,pk):
    record = get_object_or_404(Record, pk=pk)   
    # 編集対象のpkをrequestとともに受け取り、pkで該当するページを生成する。
    if request.method == "POST":
        form = RecordForm(request.POST,instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.author = request.user
            record.published_date = timezone.now()
            record.save()
            return redirect('record_detail', pk=record.pk)
    else:
        form = RecordForm(instance=record)
    return render(request, 'record/record_update.html', {'form': form})

# class RecordUpdateView(UpdateView):
#     template_name = 'record_update.html'
#     model = Record
#     fields = ('date', 'title', 'text',)
#     success_url = reverse_lazy('record/record_list')
 
#     def form_valid(self, form):
#         record = form.save(commit=False)
#         record.updated_at = timezone.now()
#         record.save()
#         return super().form_valid(form)
    
class RecordDeleteView(DeleteView):
    template_name = 'record/record_delete.html'
    model = Record
    success_url = reverse_lazy('record_list')
    