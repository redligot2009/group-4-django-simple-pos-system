from logging import log
from django.test import TestCase, Client

from .models import Order, Item, OrderItem

from django.core import exceptions
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseNotAllowed
from django.urls import reverse


"""
Model tests for:
- Order
- Item
TODO:
- Tests for OrderItem
- Tests for views
"""

class OrderTests(TestCase):
    def test_order_creation(self):
        no_test_orders = 5
        for i in range (0,no_test_orders):
            sample_order = Order.objects.create()
            sample_order.save()
        sample_orders = Order.objects.all()
        self.assertEqual(len(sample_orders),5)

    def test_order_update(self):
        sample_order = Order.objects.create()
        sample_order.save()
        sample_orders = Order.objects.all()
        self.assertEqual(len(sample_orders),1)
        sample_order = sample_orders.first()
        sample_order.total_amount_paid=30.0
        sample_order.save()
        sample_order = sample_orders.first()
        self.assertAlmostEqual(sample_order.total_amount_paid,30.0,4)
        with self.assertRaises(exceptions.ValidationError):
            sample_order.total_amount_paid="hey"
            sample_order.save()

    def test_order_delete(self):
        sample_order = Order.objects.create()
        sample_order.save()
        sample_orders = Order.objects.all()
        self.assertEqual(len(sample_orders),1)
        sample_order = sample_orders.filter(id=sample_order.id).delete()
        sample_orders = Order.objects.all()
        self.assertEqual(len(sample_orders),0)

class ItemTests(TestCase):
    def test_item_creation(self):
        no_test_items = 5
        for i in range (0,no_test_items):
            sample_item = Item.objects.create(item_price=25.0, item_name='Test Item')
            sample_item.save()
        sample_items = Item.objects.all()
        self.assertEqual(len(sample_items),5)

    def test_item_update(self):
        sample_item = Item.objects.create(item_price=25.0, item_name='Test Item')
        sample_item.save()
        sample_items = Item.objects.all()
        self.assertEqual(len(sample_items),1)
        sample_item = sample_items.first()
        sample_item.item_price=30.0
        sample_item.item_name="New Test Item"
        sample_item.save()
        sample_item = sample_items.first()
        self.assertAlmostEqual(sample_item.item_price,30.0,4)
        self.assertEqual(sample_item.item_name,"New Test Item")
        with self.assertRaises(exceptions.ValidationError):
            sample_item.item_price="hey"
            sample_item.save()

    def test_item_delete(self):
        sample_item = Item.objects.create(item_price=25.0, item_name='Test Item')
        sample_item.save()
        sample_items = Item.objects.all()
        self.assertEqual(len(sample_items),1)
        sample_item = sample_items.filter(id=sample_item.id).delete()
        sample_items = Item.objects.all()
        self.assertEqual(len(sample_items),0)

"""
Tests for views:
- create_order
- order_details
- list_orders
- update_order
"""

class ItemViewTests(TestCase):

    def test_create_item(self):
        items = Item.objects.all()
        cnt_items = len(items)
        response = self.client.post('/add_item',
            {"item_name": "Test Item",
            "item_price": 50})
        self.assertEqual(response.status_code, 302)
        items = Item.objects.all()
        self.assertTrue(len(items) > cnt_items)

    def test_update_item(self):
        self.test_create_item()
        item_to_update = Item.objects.first()
        item_pk = item_to_update.id
        response = self.client.post(reverse('update_item',kwargs={'pk':item_pk}),
            {"item_name": "Test Item A",
            "item_price": 25,
            "stock_quantity": 15})
        self.assertEqual(response.status_code, 302)
        item_to_update = Item.objects.get(id=item_pk)
        self.assertEqual(item_to_update.item_name,"Test Item A")
        self.assertEqual(item_to_update.stock_quantity,15)
        self.assertEqual(item_to_update.item_price,25)

class OrderViewTests(TestCase):

    def test_create_order(self):
        orders = Order.objects.all()
        order_cnt = len(orders)
        response = self.client.post("/orders/create")
        self.assertEqual(response.status_code, 302)
        orders = Order.objects.all()
        self.assertTrue(len(orders) > order_cnt)

