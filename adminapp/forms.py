from authapp.forms import UserRegisterForm, UserProfileForm
from authapp.models import User
from mainapp.models import Product
from django import forms
from django.forms import ModelForm
from django.db import models

class UserAdminRegistrationForm(UserRegisterForm):
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)#required=False необязательное добавление изображения
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'

class UserAdminProfileForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False

class ProductAdminRegistrationForm(ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    class Meta:
        model = Product
        fields = ('name', 'short_description', 'price', 'image', 'quantity', 'category')
    def __init__(self, *args, **kwargs):
        super(ProductAdminRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите имя продукта'
        self.fields['short_description'].widget.attrs['placeholder'] = 'Введите описание продукта'
        self.fields['price'].widget.attrs['placeholder'] = 'Введите цену товара'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Заполните колличество продуктов'
        self.fields['category'].widget.attrs['placeholder'] = 'Укажите категорию'



        for field_name, field in self.fields.items():
              field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'
    # def __init__(self, *args, **kwargs):
    #     super(UserAdminRegistrationForm, self).__init__(*args, **kwargs)
    #     self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'

class ProductAdminProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductAdminProfileForm, self).__init__(*args, **kwargs)