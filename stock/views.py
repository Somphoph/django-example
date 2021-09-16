from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import generic

from stock.models import Vendor, ReceiveOrder


class IndexView(generic.ListView):
    template_name = 'receives/index.html'
    context_object_name = 'receive_list'

    def get_queryset(self):
        return ReceiveOrder.objects.order_by('-receive_date')[:10]


class ReceiveEdit(generic.DetailView):
    model = ReceiveOrder
    template_name = 'receives/edit.html'


def receive_add(request):
    return render(request, 'receives/edit.html')


def index(request):
    latest_list = Vendor.objects.order_by('-vendor_name')[:10]
    template = loader.get_template('vendors/index.html')
    context = {
        'latest_list': latest_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'vendors/detail.html', {'vendor': vendor})
