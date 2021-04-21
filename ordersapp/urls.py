import ordersapp.views as ordersapp
from django.urls import path
from ordersapp.views import get_product_price

app_name = "ordersapp"

urlpatterns = [
    path('',
         ordersapp.OrderList.as_view(),
         name='orders_list'
         ),

    path('forming/complete/<int:pk>/',
         ordersapp.order_forming_complete,
         name='order_forming_complete'
         ),

    path('create/',
         ordersapp.OrderItemsCreate.as_view(),
         name='order_create'
         ),

    path('read/<int:pk>/',
         ordersapp.OrderRead.as_view(),
         name='order_read'
         ),

    path('update/<int:pk>/',
         ordersapp.OrderItemsUpdate.as_view(),
         name='order_update'
         ),

    path('delete/<int:pk>/',
         ordersapp.OrderDelete.as_view(),
         name='order_delete'
         ),

    path('product/<int:pk>/price/', get_product_price, name="product_price"),
]
