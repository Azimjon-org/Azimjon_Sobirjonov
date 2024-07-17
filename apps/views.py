from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, FormView, UpdateView

from apps.forms import RegisterModelForm
from apps.models import User, Product, Category


class ProductListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('log_in')
    queryset = Product.objects.all()
    template_name = 'apps/products/product-list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class RegisterFormView(FormView):
    template_name = 'apps/auth/register.html'
    success_url = 'apps/auth/login.html'
    form_class = RegisterModelForm

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect('log_in')

    def form_invalid(self, form):
        context = {
            "error_message": "User with this Phone Number already exists !"
        }
        return render(self.request, 'apps/auth/register.html', context)


class CustomLoginTemplateView(TemplateView):
    template_name = 'apps/auth/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        # phone = re.sub(r'\D', '', request.POST.get('phone_number'))
        user = User.objects.filter(email=email).first()
        if not user:
            return redirect('register')
        else:
            user = authenticate(request, username=user.email, password=request.POST['password'])
            if user:
                login(request, user)
                return redirect('main')

            else:

                context = {
                    "password_error": "Invalid password"
                }
                return render(request, template_name='apps/auth/login.html', context=context)


class CustomerEditUpdateView(UpdateView):
    queryset = User.objects.filter(status_type=User.StatusType.CUSTOMER)
    fields = 'first_name', 'last_name', 'phone_number', 'mobile_number', 'email', 'image'
    template_name = 'apps/auth/customer-edit.html'
    context_object_name = 'customer'

    def get_success_url(self):
        return reverse('customer_update', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

