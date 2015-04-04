from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from folder.views import FolderLogin, FolderLogout, FolderSignup, FolderHome, \
    FolderDeleteFile, FolderGetFile, FolderCreateSharedLink, \
    FolderDeleteSharedLink, FolderAnonymousGetSharedLink

urlpatterns = [
    url(r'^signup/$', FolderSignup.as_view()),
    url(r'^login/$', FolderLogin.as_view()),
    url(r'^logout/$', FolderLogout.as_view()),
    url(r'^home/$', login_required(FolderHome.as_view())),
    url(r'^delete/(?P<pk>\d+)$', login_required(FolderDeleteFile.as_view())),
    url(r'^download/(?P<pk>\d+)$', login_required(FolderGetFile.as_view())),
    url(r'^create_shared_link/(?P<pk>\d+)$',
        login_required(FolderCreateSharedLink.as_view())),
    url(r'^delete_shared_link/(?P<pk>\d+)$',
        login_required(FolderDeleteSharedLink.as_view())),
    url(r'shared/(?P<name>[a-zA-Z]{10})$',
        FolderAnonymousGetSharedLink.as_view()),
]
