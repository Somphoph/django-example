from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path('', views.ReceiveIndexView.as_view(), name='index'),
                  path('receives/<int:receive_id>', views.receive_edit, name='edit'),
                  path('receives/', views.receive_add, name='add'),
                  path('receives/<int:receive_id>/details/', views.receive_detail_add, name="detail_add"),
                  path('receives/<int:receive_id>/details/<int:detail_id>', views.receive_detail_edit,
                       name="detail_edit"),
                  path('receives/<int:receive_id>/details/<int:detail_id>/action/delete', views.receive_detail_delete,
                       name="detail_delete"),
                  path('deliveries/view', views.DeliveryIndexView.as_view(), name='delivery_index'),
                  path('deliveries/<int:delivery_id>', views.delivery_edit, name='delivery_edit'),
                  path('deliveries/', views.delivery_add, name='delivery_add'),
                  path('deliveries/<int:delivery_id>/details/', views.delivery_detail_add, name="delivery_detail_add"),
                  path('deliveries/<int:delivery_id>/details/<int:detail_id>', views.delivery_detail_edit,
                       name="delivery_detail_edit"),
                  path('receives/<int:delivery_id>/details/<int:detail_id>/action/delete', views.delivery_detail_delete,
                       name="delivery_detail_delete"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
