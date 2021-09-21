from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),
                  path('receive/<int:receive_id>', views.receive_edit, name='edit'),
                  path('receive/', views.receive_add, name='add'),
                  path('receive/<int:receive_id>/details/', views.receive_detail_add, name="detail_add"),
                  path('receive/<int:receive_id>/details/<int:detail_id>', views.receive_detail_edit, name="detail_edit"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
