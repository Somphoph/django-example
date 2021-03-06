from django.db.models import F, OuterRef, Subquery, Exists, Q
from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.views import generic

from stock.models import ReceiveOrder, Vendor, Product, DeliveryOrder, Customer, DeliveryOrderDetail, \
    ReceiveOrderDetail, DeliveryOrderDetailReceiveUpdate


class ReceiveIndexView(generic.ListView):
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
        vendor = get_object_or_404(Vendor, pk=post['receive_vendor'])
        receive.vendor = vendor
        receive.receive_amount = post['receive_amount']
        receive.save()
        return redirect('/receives/' + str(receive.receive_id))

    product_list = Product.objects.order_by('-product_name')
    vendor_list = Vendor.objects.order_by('-vendor_name')
    detail_list = ReceiveOrderDetail.objects.filter(
        receive=receive).order_by('-receive_detail_id')
    return render(request, 'receives/edit.html',
                  {'vendor_list': vendor_list, 'object': receive, 'detail_list': detail_list,
                   'product_list': product_list})


def receive_add(request):
    receive = ReceiveOrder()
    if request.method == 'POST':
        if not request.POST['receive_id']:
            post = request.POST
            vendor = get_object_or_404(Vendor, pk=post['receive_vendor'])
            receive = ReceiveOrder(receive_no=post['receive_no'], vendor=vendor,
                                   receive_date=post['receive_date'], receive_amount=0)
            receive.save()
            return redirect('/receives/' + str(receive.receive_id))

    vendor_list = Vendor.objects.order_by('-vendor_name')
    return render(request, 'receives/edit.html', {'vendor_list': vendor_list, 'object': receive})


def receive_detail_add(request, receive_id):
    if request.method == 'POST':
        if receive_id:
            post = request.POST
            receive = get_object_or_404(ReceiveOrder, pk=receive_id)
            detail = ReceiveOrderDetail(product_id=post['product_id'], qty=post['qty'],
                                        cost=post['cost'], po=post['po'], receive=receive)
            detail.save()
            receive = get_object_or_404(ReceiveOrder, pk=receive_id)
            update_receive_order_amount(receive_id)
            receive.save()
            return redirect('/receives/' + str(receive.receive_id))
    else:
        return HttpResponse(status=404)


def receive_detail_edit(request, receive_id, detail_id):
    if request.method == 'POST':
        if receive_id is not None:
            detail = get_object_or_404(ReceiveOrderDetail, pk=detail_id)
            post = request.POST
            detail.product_id = post['product_id']
            detail.qty = post['qty']
            detail.cost = post['cost']
            detail.po = post['po']
            detail.save()

            update_receive_order_amount(receive_id)
            return redirect('/receives/' + str(receive_id))
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)


def receive_detail_delete(request, receive_id, detail_id):
    if request.method == 'POST':
        detail = get_object_or_404(ReceiveOrderDetail, pk=detail_id)
        detail.delete()
        update_receive_order_amount(receive_id)
        return redirect('/receives/' + str(receive_id))
    else:
        return HttpResponse(status=404)


def update_receive_order_amount(receive_id):
    receive = get_object_or_404(ReceiveOrder, pk=receive_id)
    total = ReceiveOrderDetail.objects.filter(
        receive_id=receive_id).aggregate(total=Sum(F('qty') * F('cost'))).get('total')

    if total is not None:
        receive.receive_amount=total
    else:
        receive.receive_amount=0

    receive.save()


class DeliveryIndexView(generic.ListView):
    template_name = 'delivery/index.html'
    context_object_name = 'delivery_list'

    def get_queryset(self):
        return DeliveryOrder.objects.order_by('-delivery_date')[:10]


def delivery_edit(request, delivery_id):
    delivery = get_object_or_404(DeliveryOrder, pk=delivery_id)

    if request.method == 'POST':
        post = request.POST
        delivery.delivery_no = post['delivery_no']
        delivery.delivery_date = post['delivery_date']
        customer = get_object_or_404(Customer, pk=post['customer'])
        delivery.customer = customer
        delivery.save()
        return redirect('/deliveries/{0}'.format(str(delivery.delivery_id)))

    product_list = Product.objects.order_by('-product_name')
    customer_list = Customer.objects.order_by('-customer_short_name')
    detail_list = DeliveryOrderDetail.objects.filter(
        delivery_id=delivery_id).order_by('-delivery_detail_id')
    subquery = DeliveryOrderDetailReceiveUpdate.objects.filter(receive_detail=OuterRef("pk"))[:1].values(
        'sum_of_delivery_detail_qty')
    receive_detail_list = ReceiveOrderDetail.objects.filter(
        Q(qty__gt=Subquery(subquery)) | Q(~Exists(subquery))).order_by('-receive_detail_id')
    print(receive_detail_list.query)
    return render(request, 'delivery/edit.html',
                  {'customer_list': customer_list, 'object': delivery, 'detail_list': detail_list,
                   'product_list': product_list, 'receive_detail_list': receive_detail_list})


def delivery_add(request):
    obj = DeliveryOrder()
    if request.method == 'POST':
        if not request.POST['delivery_id']:
            post = request.POST
            customer = get_object_or_404(Customer, pk=post['customer'])
            obj = DeliveryOrder(delivery_no=post['delivery_no'], customer=customer,
                                delivery_date=post['delivery_date'])
            obj.save()
            return redirect('/deliveries/' + str(obj.delivery_id))

    customer_list = Customer.objects.order_by('-customer_short_name')
    return render(request, 'delivery/edit.html', {'customer_list': customer_list, 'object': obj})


def delivery_detail_add(request, delivery_id):
    if request.method == 'POST':
        if delivery_id:
            post = request.POST
            product = get_object_or_404(Product, pk=post['product_id'])
            detail = DeliveryOrderDetail(product=product, qty=post['qty'],
                                         price=post['price'], so=post['so'], delivery_id=delivery_id,
                                         receive_detail_id=post['receive_detail_id'])
            detail.save()
            obj = get_object_or_404(DeliveryOrder, pk=delivery_id)
            obj.save()
            update_delivery_amount(delivery_id)
            return redirect('/deliveries/' + str(obj.delivery_id))
    else:
        return HttpResponse(status=404)


def delivery_detail_edit(request, delivery_id, detail_id):
    if request.method == 'POST':
        if delivery_id is not None:
            detail = get_object_or_404(DeliveryOrderDetail, pk=detail_id)
            post = request.POST
            detail.product_id = post['product_id']
            detail.qty = post['qty']
            detail.price = post['price']
            detail.so = post['so']
            detail.receive_detail_id = post['receive_detail_id']
            detail.save()
            update_delivery_amount(delivery_id)
            return redirect('/deliveries/' + str(delivery_id))
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)


def delivery_detail_delete(request, delivery_id, detail_id):
    if request.method == 'POST':
        detail = get_object_or_404(DeliveryOrderDetail, pk=detail_id)
        detail.delete()
        update_delivery_amount(delivery_id)
        return redirect('/deliveries/' + str(delivery_id))
    else:
        return HttpResponse(status=404)


def update_delivery_amount(delivery_id):
    detail_list = DeliveryOrderDetail.objects.filter(delivery_id=delivery_id)
    for detail in detail_list:
        total = DeliveryOrderDetail.objects.filter(receive_detail_id=detail.receive_detail_id).aggregate(
            total=Sum('qty')).get('total')
        update = DeliveryOrderDetailReceiveUpdate(receive_detail_id=detail.receive_detail_id,
                                                  sum_of_delivery_detail_qty=total)
        update.save()


def index(request):
    latest_list = Vendor.objects.order_by('-vendor_name')[:10]
    template = loader.get_template('vendors/index.html')
    context = {
        'latest_list': latest_list,
    }
    return HttpResponse(template.render(context, request))


def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'vendors/detail.html', {'vendor': vendor})
