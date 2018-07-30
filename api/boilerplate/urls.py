
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/admin/', admin.site.urls),
    url(r'^api/v1/chatbot/$', views.MessageList.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)