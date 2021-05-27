from django.test import TestCase

from .models import Order, Item, OrderItem

from django.core import exceptions

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