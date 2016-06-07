from django.conf.urls import url
from api.public_files import views


urlpatterns = [
    url(r'^(?P<user_id>\w+)/$', views.PublicFileDetail.as_view(), name=views.PublicFileDetail.view_name),
    url(r'^(?P<user_id>\w+)/content/$', views.PublicFileContent.as_view(), name=views.PublicFileContent.view_name),
]
