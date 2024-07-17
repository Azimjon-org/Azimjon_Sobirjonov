from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.views import ProductListView, CustomLoginTemplateView, RegisterFormView, CustomerEditUpdateView

urlpatterns = [
    path('', ProductListView.as_view(), name='main'),
    path('update/<int:pk>', CustomerEditUpdateView.as_view(), name='customer_update')
]

urlpatterns += [
    path('log_in/', CustomLoginTemplateView.as_view(), name='log_in'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('log_out/', LogoutView.as_view(), name='log_out'),

]
