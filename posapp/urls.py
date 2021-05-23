from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.index, name='index'),
    path('configure_items',views.configure_items,name='configure_items'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('add_item', views.add_item, name='add_item'),
    path('update_item/<int:pk>/',views.update_item,name='update_item'),
    path('orders',views.list_orders,name='list_orders'),
    path('orders/create', views.create_order, name='create_order'),
    path('order/<int:pk>/', views.order_details, name='order_details'),
    path('order/<int:pk>/update', views.update_order, name='update_order'),
    path('order/<int:pk>/delete', views.delete_order, name='delete_order'),
    path('order/<int:pk>/add_item',views.add_order_item, name='add_order_item')
]