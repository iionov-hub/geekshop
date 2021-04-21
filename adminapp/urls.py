from django.urls import path

from adminapp.views import UserCreateView,UserListView, index, UserUpdateView, UserDeleteView, admin_products, admin_products_create, admin_products_update, admin_products_delete

app_name = 'adminapp'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('products/', admin_products, name='admin_products'),
    # path('users-create/', admin_users_create, name='admin_users_create'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('products-create/', admin_products_create, name='admin_products_create'),
    # path('users-update/<int:user_id>/', admin_users_update, name='admin_users_update'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('products-update/<int:product_id>/', admin_products_update, name='admin_products_update'),
    # path('users-delete/<int:user_id>/', admin_users_delete, name='admin_users_delete'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
    path('products-delete/<int:product_id>/', admin_products_delete, name='admin_products_delete'),
]