from django.db.models import fields, F
from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.views import generic

from stock.models import Product, ReceiveOrderDetail, Vendor, ReceiveOrder


class IndexView(generic.ListView):
    template_name = 'receives/index.html'
    context_object_name = 'receive_list'

    def get_queryset(self):
        return ReceiveOrder.objects.order_by('-receive_date')[:10]


def receive_edit(request, receive_id):
    receive = get_object_or_404(ReceiveOrder, pk=receive_id)

    if request.method == 'POST':
        post = request.POST
        receive.receive_no = post['receive_no']
        receive.receive_date = post['receive_date']
        receive.receive_vendor = post['receive_vendor']
        receive.receive_amount = post['receive_amount']
        receive.save()
        return redirect('/receive/' + str(receive.receive_id))

    product_list = Product.objects.order_by('-product_name')
    vendor_list = Vendor.objects.order_by('-vendor_name')
    detail_list = ReceiveOrderDetail.objects.filter(
        receive_id=receive_id).order_by('-receive_detail_id')
    return render(request, 'receives/edit.html',
                  {'vendor_list': vendor_list, 'object': receive, 'detail_list': detail_list,
                   'product_list': product_list})


def receive_add(request):
    receive = ReceiveOrder()
    if request.method == 'POST':
        if not request.POST['receive_id']:
            post = request.POST
            receive = ReceiveOrder(receive_no=post['receive_no'], receive_vendor=post['receive_vendor'],
                                   receive_date=post['receive_date'], receive_amount=0)
            receive.save()

    vendor_list = Vendor.objects.order_by('-vendor_name')
    return render(request, 'receives/edit.html', {'vendor_list': vendor_list, 'object': receive})


def receive_detail_add(request, receive_id):
    if request.method == 'POST':
        if receive_id:
            post = request.POST
            detail = ReceiveOrderDetail(product_id=post['product_id'], qty=post['qty'],
                                        cost=post['cost'], po=post['po'], receive_id=receive_id)
            detail.save()
            receive = get_object_or_404(ReceiveOrder, pk=receive_id)
            receive.receive_amount = ReceiveOrderDetail.objects.filter(
                receive_id=receive_id).aggregate(total=Sum(F('qty') * F('cost'))).get('total')
            receive.save()
            return redirect('/receive/' + str(receive.receive_id))
    else:
        return HttpResponse(status=404)


def receive_detail_edit(request, detail_id):
    if request.method == 'POST':
        if not request.POST['receive_id']:
            detail = get_object_or_404(ReceiveOrderDetail, pk=detail_id)
            post = request.POST
            detail = ReceiveOrderDetail(product_id=post['product_id'], qty=post['qty'],
                                        cost=post['cost'], po=post['po'])
            detail.save()
            receive = get_object_or_404(ReceiveOrder, pk=detail.receive_id)
            receive.receive_amount = ReceiveOrderDetail.objects.filter(
                receive_id=detail.receive_id).aggregate(total=Sum('amount', field="qty * cost"))['total']
            receive.save()
            return redirect('/receive/' + str(receive.receive_id))
    else:
        return HttpResponse(status=404)


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
