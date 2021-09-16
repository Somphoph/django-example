from django.urls import path

from . import views

urlpatterns = {
    path('', views.IndexView.as_view(), name='index'),
    path('receive/<int:pk>', views.ReceiveEdit.as_view(), name='receive'),
    path('receive', views.receive_add, name='receive'),
}
