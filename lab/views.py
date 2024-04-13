from typing import Any
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from . models import Item, Lab, ItemGroup
from . utils import get_total_item_qty
from .forms import LabCreateForm


class LabListView(generic.ListView):
    template_name = "lab/labs-list.html"
    queryset = Lab.objects.all()
    context_object_name = 'labs'
    ordering = ['-id']
    

class LabDetailView(generic.DetailView):
    template_name = "lab/lab-detail.html"
    model = Lab
    context_object_name = "lab"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
        items = Item.objects.filter(lab=lab)
        groups = ItemGroup.objects.filter(lab=lab)
        context["items"] = items
        context["groups"] = groups
        return context
    

class LabCreateView(generic.CreateView):
    model = Lab
    form_class = LabCreateForm
    template_name = "lab/lab-create.html"
    
    def get_success_url(self):
        lab = self.object
        return reverse('lab:lab-detail', kwargs={'pk': lab.pk})
    
    def form_valid(self, form):
        selected_users = form.cleaned_data['users']
        lab = form.save(commit=False)
        lab.save()
        lab.user.set(selected_users)
        return super().form_valid(form)
    

class UpdateLabView(generic.UpdateView):
    template_name = 'lab/lab-update.html'
    model = Lab
    form_class = LabCreateForm
    
    def get_form(self):
        form = super().get_form()
        lab = self.get_object()
        form.fields['users'].initial = lab.user.all()
        return form
    
    def form_valid(self, form):
        selected_users = form.cleaned_data['users']
        lab = form.save(commit=False)
        lab.user.set(selected_users)
        lab.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        lab = self.object
        return reverse('lab:lab-detail', kwargs={'pk': lab.pk})
    
    
class DeleteLabView(generic.DeleteView):
    model = Lab
    template_name = "lab/lab-delete.html"
    
    def get_success_url(self):
        return reverse('lab:lab-list')
    

class CreateItemView(generic.CreateView):
    template_name = 'lab/add-item.html'
    model = Item    
    fields = ["item_name", "qty", "unit_of_measure", "category"]
    
    def form_valid(self, form):
        item = form.save(commit=False)
        labid = self.kwargs["pk"]
        item_group_id = self.kwargs["itemgroup_id"]
        lab = Lab.objects.get(pk=labid)
        item.lab = lab
        item.save()
        item_group = ItemGroup.objects.get(pk=item_group_id)
        item_group.items.add(item)
        return super().form_valid(form)

    def get_success_url(self):
        lab_pk = self.kwargs["pk"]
        item_group_id = self.kwargs["itemgroup_id"]
        return reverse('lab:group-detail', kwargs={'pk': lab_pk, "itemgroup_id" : item_group_id})


class ItemUpdateView(generic.UpdateView):
    model = Item
    template_name = "lab/item-update.html"
    fields = "__all__"
    
    def get_object(self, queryset=None):
        item_id = self.kwargs['item_id']
        queryset = self.get_queryset()
        return queryset.get(pk=item_id)
    
    def get_success_url(self):
        lab_pk = self.kwargs["pk"]
        return reverse('lab:lab-detail', kwargs={'pk': lab_pk})
    

class ItemGroupCreateView(generic.CreateView):
    template_name = 'lab/create-group.html'
    model = ItemGroup
    fields = ["group_name"]
    
    def form_valid(self, form):
        item_group = form.save(commit=False)
        labid = self.kwargs["pk"]
        lab = Lab.objects.get(pk=labid)
        item_group.lab = lab
        item_group.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        lab_pk = self.kwargs["pk"]
        return reverse('lab:lab-detail', kwargs={'pk': lab_pk})


class ItemGroupDetailView(generic.DetailView):
    model = ItemGroup
    template_name = 'lab/item-group-detail.html'
    context_object_name = 'item_group'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_group = get_object_or_404(ItemGroup, pk=self.kwargs['itemgroup_id'])
        context["item_group"] = item_group
        return context  
    