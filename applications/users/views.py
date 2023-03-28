from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
# from applications.users.decorators import registrar_auditoria
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from django.views.generic import (
    View,
    CreateView,
    ListView,
)

from django.views.generic.edit import (
    FormView,
)

from .forms import (
    UserRegisterForm, 
    LoginForm,
    UpdatePasswordForm,
    VerificationForm
)
#
from .models import User
from applications.permisos.models import ConfEmpresas
# 
from .functions import code_generator


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        # generamos el codigo
        # codigo = code_generator()
        #
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            # codregistro=codigo
        )
        # # enviar el codigo al email del user
        # asunto = 'Confirmación de email'
        # mensaje = 'Codigo de verificación: ' + codigo
        # email_remitente = 'torredecontrolamovil@gmail.com'
        # #
        # send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        # # redirigir a pantalla de valdiacion

        # return HttpResponseRedirect(
        #     reverse(
        #         'users_app:user-verification',
        #         kwargs={'pk': usuario.id}
        #     )
        # )
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )
      


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        #
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        return super(CodeVerificationView, self).form_valid(form)

class DatabaseView(ListView):
    model = ConfEmpresas
    template_name = 'includes/database_list.html'

    def get_queryset(self):
        return self.request.user.conf_empresas.all()

def database_list(request):
    databases = request.user.conf_empresas.all()
    database_list = [database.name for database in databases]
    return JsonResponse({'database_list': database_list})


