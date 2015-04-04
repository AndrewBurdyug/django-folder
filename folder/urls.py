from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from folder.views import FolderLogin, FolderLogout, FolderSignup, FolderHome, \
    FolderDeleteFile, FolderGetFile

urlpatterns = [
    url(r'^signup/$', FolderSignup.as_view()),
    url(r'^login/$', FolderLogin.as_view()),
    url(r'^logout/$', FolderLogout.as_view()),
    url(r'^home/$', login_required(FolderHome.as_view())),
    url(r'^delete/(?P<pk>\d+)$', login_required(FolderDeleteFile.as_view())),
    url(r'^download/(?P<pk>\d+)$', login_required(FolderGetFile.as_view())),
]
