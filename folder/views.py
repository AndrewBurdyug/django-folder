from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.views.generic import View
from django.conf import settings

from folder.forms import FolderUserCreationFrom

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
                                     'info': 'User is active'})
            else:
                return JsonResponse({'status': 'ERROR',
                                     'info': 'User inactive'})
        else:
            return JsonResponse({'status': 'ERROR',
                                 'info': 'Invalid login'})


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
                                 'info': 'Registered'})
        else:
            return JsonResponse({'status': 'ERROR',
                                 'info': '%s' % form.errors})


class FolderHome(View):
    template_name = 'folder/home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass
