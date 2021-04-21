from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView #ListView класс для просмотра
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from authapp.models import User
from mainapp.models import Product
from adminapp.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdminRegistrationForm, ProductAdminProfileForm

# Create your views here.
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def index(request):
    return render(request, 'adminapp/index.html')

#read

class UserListView(ListView):#ListView класс для просмотра
    model = User
    template_name = 'adminapp/admin-users-read.html'

    #проверяем на суперюзера если нет, то не сможем открыть страницу
    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'))
    # Метод на октрывание страниц
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)

    # queryset = User.objects.filter(is_active=True)# выбираем по определенным условия (например только активных пользователей)
# @user_passes_test(lambda u: u.is_superuser, login_url='/')
# def admin_users(request):
#     context = {'users': User.objects.all()}
#     return render(request, 'adminapp/admin-users-read.html', context)

#create
class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admin_staff:admin_users')
# @user_passes_test(lambda u: u.is_superuser, login_url='/')
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminRegistrationForm()
#     context = {'form': form}
#     return render(request, 'adminapp/admin-users-create.html', context)

#update
class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admin_staff:admin_users')

    # передаем в контекст title
    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Редактирование'
        return context

# @user_passes_test(lambda u: u.is_superuser, login_url='/')
# def admin_users_update(request, user_id):
#     user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=user)
#
#
#     context = {'form': form, 'user': user}
#     return render(request, 'adminapp/admin-users-update-delete.html', context)

#delete

class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active == True:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
# @user_passes_test(lambda u: u.is_superuser, login_url='/')
# def admin_users_delete(request, user_id):
#     user = User.objects.get(id=user_id)
#     #user.delete() удаление из базы
#
#     if user.is_active == True:
#         user.is_active = False
#     else:
#         user.is_active = True
#
#     user.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_users'))

def admin_products(request):
    context = {'products': Product.objects.all()}
    return render(request, 'adminapp/admin-products-read.html', context)

#create
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def admin_products_create(request):
    if request.method == 'POST':
        form = ProductAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_products'))
    else:
        form = ProductAdminRegistrationForm()
    context = {'form': form}
    return render(request, 'adminapp/admin-products-create.html', context)

#update products
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def admin_products_update(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductAdminRegistrationForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_products'))
    else:
        form = ProductAdminRegistrationForm(instance=product)


    context = {'form': form, 'product': product}
    return render(request, 'adminapp/admin-products-update-delete.html', context)

#delete product
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def admin_products_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    print(product)
    product.delete()
    return HttpResponseRedirect(reverse('admin_staff:admin_products'))