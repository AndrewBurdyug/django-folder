from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.views.generic import View
from django.conf import settings

from folder.forms import FolderUserCreationFrom, UploadFileForm
from folder.utils import dehydrate_validation_errors, handle_uploaded_file
from folder.errors import BadData
from folder.models import FileLink

FOLDER_SIGNUP_ENABLED = True
if hasattr(settings, 'FOLDER_SIGNUP_ENABLED'):
    FOLDER_SIGNUP_ENABLED = settings.FOLDER_SIGNUP_ENABLED

extra_permissions = [
    Permission.objects.get(codename=x) for x in
    ('add_file', 'change_file', 'delete_file',
     'add_filelink', 'change_filelink', 'delete_filelink')
]


class FolderLogin(View):
    template_name = 'folder/login.html'

    def get(self, request):
        context = {'FOLDER_SIGNUP_ENABLED': FOLDER_SIGNUP_ENABLED}
        context.update(csrf(request))
        return render_to_response(self.template_name, context)

    def post(self, request):
        username = request.POST.get('username', 'EMPTY_USER')
        password = request.POST.get('password', 'EMPTY_PASS')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'status': 'OK',
                                     'info': {'username': 'User is active'}})
            else:
                return JsonResponse({'status': 'ERROR',
                                     'info': {'username': 'User inactive'}})
        else:
            return JsonResponse({'status': 'ERROR',
                                 'info': {'username/password': 'Invalid'}})


class FolderLogout(View):

    def get(self, request):
        logout(request)
        return redirect('/folder/login/')


class FolderSignup(View):
    template_name = 'folder/signup.html'

    def get(self, request):
        if FOLDER_SIGNUP_ENABLED:
            return render(request, self.template_name)
        return redirect('/folder/login/')

    def post(self, request):
        form = FolderUserCreationFrom(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.user_permissions.add(*extra_permissions)
            return JsonResponse({'status': 'OK',
                                 'info': {'username': 'Registered'}})
        else:
            validation_errors = dehydrate_validation_errors(
                form.errors.as_data()
            )
            return JsonResponse({'status': 'ERROR',
                                 'info': validation_errors})


class FolderHome(View):
    template_name = 'folder/home.html'

    def get(self, request, extra_context={}):
        form = UploadFileForm()
        context = {'form': form, 'user': request.user,
                   'files': FileLink.objects.filter(owner=request.user)}
        context.update(csrf(request))
        if extra_context:
            context.update(extra_context)
        return render_to_response(self.template_name, context)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                info = handle_uploaded_file(request.FILES['data'],
                                            request.user)
                return JsonResponse({'status': 'OK',
                                     'info': info})
            except BadData as er:
                return JsonResponse({'status': 'ERROR',
                                     'info': {'data': '%s' % er}})
        else:
            validation_errors = dehydrate_validation_errors(
                form.errors.as_data()
            )
            return JsonResponse({'status': 'ERROR',
                                 'info': validation_errors})
