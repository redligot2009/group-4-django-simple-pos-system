from django.http.response import Http404, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from .models import Item, Order, OrderItem
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    try:
        return render(request,'posapp/index.html')
    except:
        return HttpResponseNotFound

def configure_items(request):
    try:
        all_items = Item.objects.all()
        context = {}
        if(request.method=="POST" and request.is_ajax()):
            id = request.POST.get("id")
            item = all_items.get(id=id)
            context['item'] = item
        context['items'] = all_items
        return render(request,'posapp/configure_items.html',context)
    except:
        return HttpResponseBadRequest

def add_item(request):
    if(request.method == "POST"):
        try:
            item_name = request.POST.get("item_name")
            item_price = request.POST.get("item_price")
            Item.objects.create(item_name=item_name, item_price=item_price)
            return redirect('configure_items')
        except:
            return HttpResponseBadRequest
    else:
        return HttpResponseNotAllowed

def delete_item(request, pk):
    try:
        Item.objects.filter(pk=pk).delete()
        return redirect('configure_items')
    except:
        return HttpResponseBadRequest

def update_item(request,pk):
    if(request.method=="POST"):
        try:
            item_name = request.POST.get("item_name")
            item_price = request.POST.get("item_price")
            stock_quantity = request.POST.get("stock_quantity")
            to_update = Item.objects.get(pk=pk)
            to_update.item_name = item_name
            to_update.item_price = item_price
            to_update.stock_quantity = stock_quantity
            to_update.save()
            return redirect('configure_items')
        except:
            return HttpResponseBadRequest
    else:
        return HttpResponseNotAllowed

def create_order(request):
    # Create new order with order items passed in the request object.
    try:
        new_order = Order.objects.create()
        new_order.save()
        return redirect('order_details',pk=new_order.id)
    except:
        return HttpResponseBadRequest

def order_details(request, pk):
    # Update order data with particular pk based on request object data.
    try:
        order = Order.objects.get(pk=pk)
        running_total = 0
        for order_item in order.orderitem_set.all():
            running_total += order_item.line_total
        order.total_amount_paid = running_total
        order.save()
        all_items = Item.objects.all()
        return render(request,'posapp/order_details.html',{
            'order': order,
            'items': all_items,
        })
    except:
        return HttpResponseNotFound

def list_orders(request):
    # List down all orders
    try:
        all_orders = Order.objects.all()
        return render(request,'posapp/list_orders.html', { 'orders' : all_orders })
    except:
        return HttpResponseNotFound

def update_order(request, pk):
    order = Order.objects.get(pk=pk)
    if(request.method=="POST"):
        try:
            running_total = 0
            for item_data in request.POST.getlist('items'):
                order_item = OrderItem.objects.get_or_create(pk=item_data.pk)
                order_item.item_type = Item.objects.get(id=item_data.item_id)
                order_item.order = order
                order_item.quantity = int(item_data.quantity)
                order_item.line_amount = float(order_item.quantity) * float(order_item.item_type.item_price)
                order_item.save()
                running_total += order_item.line_amount    
            order.total_amount_paid = running_total
            order.payment_type = request.POST.get('payment_type')
            order.save()
            return redirect('order_details',pk=order.id)
        except:
            return HttpResponseServerError
    else:
        return HttpResponseNotAllowed


def add_order_item(request,pk):
    order = Order.objects.get(pk=pk)
    if(request.method=="POST"):
        order_item_quantity = int(request.POST.get("item-quantity"))
        item = get_object_or_404(klass=Item,pk=request.POST.get("item-id"))
        if(order_item_quantity > 0 and order_item_quantity <= item.stock_quantity):
            item.stock_quantity -= order_item_quantity
            new_order_item = OrderItem.objects.create(order=order,
                                                        item_type=item, 
                                                        quantity=order_item_quantity, 
                                                        line_total=order_item_quantity*item.item_price)
            item.save()
            order.save()
            return redirect('order_details',pk=order.id)
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed

def delete_order(request,pk):
    try:
        Order.objects.filter(pk=pk).delete()
        return redirect('list_orders')
    except:
        return HttpResponseBadRequest