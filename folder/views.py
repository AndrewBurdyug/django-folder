import os

from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.views.generic import View
from django.conf import settings
from django.template.defaultfilters import truncatechars

from folder.forms import FolderUserCreationFrom, UploadFileForm
from folder.utils import dehydrate_validation_errors, handle_uploaded_file, \
    generate_random_phrase
from folder.errors import BadFileSize, TooMuchFiles
from folder.models import FileLink, FileSharedLink

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
        if request.user.is_authenticated():
            return redirect('/folder/home/')

        context = {'FOLDER_SIGNUP_ENABLED': FOLDER_SIGNUP_ENABLED}
        context.update(csrf(request))
        return render_to_response(self.template_name, context)

    def post(self, request):
        if request.user.is_authenticated():
            return JsonResponse(
                {'status': 'OK',
                 'info': {'username': 'Already authenticated'}})

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
            if request.user.is_authenticated():
                return redirect('/folder/home/')
            return render(request, self.template_name)
        return redirect('/folder/login/')

    def post(self, request):
        if request.user.is_authenticated():
            return JsonResponse({'status': 'OK',
                                 'info': {'username': 'Already registered'}})

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
            except (BadFileSize, TooMuchFiles) as er:
                return JsonResponse({'status': 'ERROR',
                                     'info': {'data': '%s' % er}})
        else:
            validation_errors = dehydrate_validation_errors(
                form.errors.as_data()
            )
            return JsonResponse({'status': 'ERROR',
                                 'info': validation_errors})


class FolderDeleteFile(View):

    def post(self, request, pk):
        try:
            file_link = FileLink.objects.get(owner=request.user, pk=pk)
        except FileLink.DoesNotExists:
            pass
        else:
            # delete user file_link (safe operation)
            file_obj = file_link.target
            if file_link.shared:
                file_link.shared.delete()
            file_link.delete()

            # if file not has links - delete file
            if not file_obj.filelinks.all():

                # get physical path of file
                file_path = file_obj.name

                # if file exists - delete him
                if os.path.isfile(file_path):
                    os.unlink(file_path)

                file_obj.delete()

        return JsonResponse({'status': 'OK',
                             'info': {'file': 'Deleted'}})


class FolderGetFile(View):

    def get(self, request, pk):
        try:
            file_link = FileLink.objects.get(owner=request.user, pk=pk)
        except FileLink.DoesNotExists:
            return redirect('/folder/home/')

        file_path = file_link.target.name
        file_content_type = file_link.target.content_type
        file_name = file_link.name.encode('utf-8')

        if not os.path.isfile(file_path):
            return redirect('/folder/home/')

        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type=file_content_type)
            response['Content-Disposition'] = 'attachment; filename="%s"' % \
                file_name
            return response


class FolderCreateSharedLink(View):

    def get(self, request, pk):
        try:
            file_link = FileLink.objects.get(owner=request.user, pk=pk)
        except FileLink.DoesNotExists:
            return JsonResponse({'status': 'WARNING',
                                 'info': {'file_link': 'Not found'}})

        # if shared link already created, then just return it
        if file_link.shared:
            return JsonResponse(
                {'status': 'OK',
                 'info': {'shared_link': file_link.shared.name,
                          'created': False, 'file_link_id': file_link.pk,
                          'file_link_name': truncatechars(file_link.name, 16)}}
            )

        # create unique shared link
        created = False
        while not created:
            random_phrase = generate_random_phrase()
            shared_link, created = FileSharedLink.objects.get_or_create(
                name=random_phrase)

        # attach new shared link to the filelink
        file_link.shared = shared_link
        file_link.save()

        return JsonResponse(
            {'status': 'OK',
             'info': {'shared_link': shared_link.name, 'created': True,
                      'file_link_id': file_link.pk,
                      'file_link_name': truncatechars(file_link.name, 16)}}
        )


class FolderDeleteSharedLink(View):

    def get(self, request, pk):
        try:
            file_link = FileLink.objects.get(owner=request.user, pk=pk)
        except FileLink.DoesNotExists:
            return JsonResponse({'status': 'WARNING',
                                 'info': {'file_link': 'Not found'}})

        if file_link.shared is not None:
            file_link.shared.delete()
            file_link.shared = None
            file_link.save()
            return JsonResponse({'status': 'OK',
                                 'info': {'shared_link': 'Deleted'}})
        else:
            return JsonResponse(
                {'status': 'OK',
                 'info': {'shared_link': 'Empty, not need to delete'}})


class FolderAnonymousGetSharedLink(View):

    def get(self, request, name):
        try:
            shared_link = FileSharedLink.objects.get(name=name)
        except FileLink.DoesNotExists:
            return HttpResponseNotFound('404 File not found!')

        file_link = shared_link.filelink

        # !!! refactoring needed: below code from FolderGetFile !!!
        file_path = file_link.target.name
        file_content_type = file_link.target.content_type
        file_name = file_link.name.encode('utf-8')

        if not os.path.isfile(file_path):
            return redirect('/folder/home/')

        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type=file_content_type)
            response['Content-Disposition'] = 'filename="%s"' % \
                file_name
            return response
