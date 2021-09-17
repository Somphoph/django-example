from django.urls import path

from . import views

urlpatterns = {
    path('', views.IndexView.as_view(), name='index'),
    path('receive/<int:receive_id>', views.receive_edit, name='edit'),
    path('receive', views.receive_add, name='add'),
}
