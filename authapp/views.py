from django.core.mail import send_mail
from django.conf import settings
from authapp.models import User
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required
from django.db import transaction
from authapp.forms import UserProfileEditForm, UserProfileForm
from django.views.generic import FormView, UpdateView


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
    print(user.email)
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email,], fail_silently=False)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'authapp/login.html', context)


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                messages.success(request, 'сообщение подтверждения отправлено!')
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                messages.success(request, 'ошибка отправки сообщения!')
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))

    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'authapp/register.html', context)

# class RegisterView(FormView):
#     model = User
#     form_class = UserRegisterForm
#     template_name = 'authapp/register.html'
#     success_url = reverse_lazy('auth:login')
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(data=request.POST)
#
#         if form.is_valid():
#             user = form.save()
#             if self.send_verify_mail(user):
#                 messages.success(request, 'Вы успешно зарегистрировались! Проверьте почту. Активируйте учетную запись.')
#                 return redirect(self.success_url)
#
#             return redirect(self.success_url)
#
#         return render(request, self.template_name, {'form': form})
#
#     def send_verify_mail(self, user):
#         verify_link = reverse_lazy('authapp:verify', args=[user.email, user.activation_key])
#
#         title = f'Для активации учетной записи {user.username} пройдите по ссылке'
#
#         messages = f'Для подтверждения учетной записи {user.username} пройдите по ссылке: \n{settings.DOMAIN_NAME}' \
#                    f'{verify_link}'
#         print(user.email)
#         return send_mail(title, messages, settings.EMAIL_HOST_USER, [user.email,], fail_silently=False)
#
#     def verify(self, email, activation_key):
#         try:
#             user = User.objects.get(email=email)
#             if user.activation_key == activation_key and not user.is_activation_key_expired():
#                 user.is_active = True
#                 user.save()
#                 auth.login(self, user)
#                 return render(self, 'authapp/verification.html')
#             else:
#                 print(f'error activation user: {user}')
#                 return render(self, 'authapp/verification.html')
#         except Exception as e:
#             print(f'error activation user : {e.args}')
#             return HttpResponseRedirect(reverse('index'))



# @login_required
# def profile(request):
#     user = request.user
#     print('s')
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
#         print('s2')
#         if form.is_valid():
#             print('s3')
#             form.save()
#             return HttpResponseRedirect(reverse('auth:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#
#     baskets = Basket.objects.filter(user=user)
#     # total_quantity = sum(basket.quantity for basket in baskets)
#     # total_sum = sum(basket.sum() for basket in baskets)
#
#     context = {
#         'form': form,
#         'baskets': baskets,
#     }
#     return render(request, 'authapp/profile.html', context)


@transaction.atomic
# def edit(request):
def profile(request):
    user = request.user
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        edit_form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(
            instance=request.user.userprofile
        )
    baskets = Basket.objects.filter(user=user)
    content = {
        'title': title,
        'form': edit_form,
        'baskets': baskets,
        'profile_form': profile_form
    }

    return render(request, 'authapp/profile.html', content)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))



