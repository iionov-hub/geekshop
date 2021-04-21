from django.urls import path

from authapp.views import login, register, logout, profile
# from authapp.views import login, RegisterView, logout, profile
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<email>/<activation_key>/', authapp.verify, name='verify'),
]

# urlpatterns = [
#     path('login/', login, name='login'),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('profile/', profile, name='profile'),
#     path('logout/', logout, name='logout'),
#     path('verify/<email>/<activation_key>/', RegisterView.verify, name='verify'),
# ]

# urlpatterns = [
#     path('login/', GeekLoginView.as_view(), name='login'),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('profile/', profile, name='profile'),
#     path('logout/', logout, name='logout'),
#     path('verify/<str:email>/<str:activation_key>/', RegisterView.verify, name='verify'),
# ]