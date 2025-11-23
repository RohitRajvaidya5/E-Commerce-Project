from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('products.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')), 
     

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
