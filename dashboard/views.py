from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from dashboard.forms import UserRegistrationForm


class LoginTemplateView(LoginView):
    template_name = 'auth/login.html'  # Kullanıcı giriş formunun görüntüleneceği şablon
    success_url = reverse_lazy('index')  # Başarılı giriş sonrası yönlendirilecek URL

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(*args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, "Geçersiz eposta veya şifre.")
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


class LogoutView(LogoutView):
    next_page = reverse_lazy(
        'login')


class RegisterTemplateView(FormView):
    template_name = 'auth/register.html'  # Kayıt formunun görüntüleneceği şablon
    form_class = UserRegistrationForm  # Özel kullanıcı kayıt formu
    success_url = reverse_lazy(
        'login')  # Başarılı kayıt sonrası yönlendirilecek URL

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(*args, **kwargs)

    # eğer form geçerliyse çalışacak fonksiyon
    def form_valid(self, form):
        form.save(commit=False)
        user = form.instance
        user.username = user.email # kullanıcın username ve email alanlarını aynı yapıyorum
        user.save()
        user.staff.team_id = int(form.data.get("team"))
        user.staff.save()

        messages.success(self.request,
                         "Başarıyla kayıt oldunuz. Şimdi giriş yapabilirsiniz")

        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if request.user.staff.team.is_assembler:
            return redirect("drone_list")

        return render(request, "dashboard/index.html")

class DroneListTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'dashboard/drones.html'

class ProduceDroneTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'dashboard/create_drone.html'