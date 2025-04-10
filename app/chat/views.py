from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import View, TemplateView, ListView

from typing import Dict, Any

from .forms import RegistrationForm, LoginForm, PFPForm
from .models import User, PFP, ChatGroup


def lazy_background_video(request):
    """
    sends back partial with a video for background. Used within base.html file.
    """
    return render(request, "chat/partials/lazy_bg_video_partial.html")


"""
Authentication view classes and methods
"""


# also used by RegistrationView
def login_user_if_exists(request, form: Form) -> bool:
    user = authenticate(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password'],
    )
    if user:
        login(request, user)
        messages.success(request, 'Login succeeded!')
        return True
    return False

def redirect_to_me(request):
    """
    Redirects to the current user profile page
    """
    if request.user.is_authenticated:
        return redirect('chat:user_profile_self')
    else:
        messages.error(request, 'You have to be authenticated!')
        return redirect('chat:login')

class LoginView(View):
    # Login view class
    template_name = 'chat/login.html'

    def get(self, request):
        return render(request, self.template_name, context={'form': LoginForm})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            if login_user_if_exists(request, form):
                redirect_to = request.POST.get('next')
                if redirect_to:
                    return redirect(redirect_to)

                return redirect('chat:user_profile_self')

        messages.error(request, 'Login failed!')
        return render(request, self.template_name, context={'form': form})


def user_logout(request):
    logout(request)

    messages.success(request, 'You have successfully logged out!')
    return redirect('chat:login')


class RegistrationView(View):
    # Registration view class
    template_name = 'chat/register.html'

    def get(self, request):
        return render(request, self.template_name, context={'form': RegistrationForm})

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )

            messages.success(request, 'Registration success!')

            if login_user_if_exists(request, form):
                return redirect('chat:home')

        messages.error(request, 'Registration failed!')
        return render(request, self.template_name, context={'form': form})


"""
Home view class and methods
"""


@login_required(login_url=reverse_lazy('chat:login'))
@require_http_methods(["POST"])
def change_pfp(request):
    """
    Method to change profile picture. Image should be less than 1mb and has JPG, JPEG, PNG.
    """
    pfp = get_object_or_404(PFP, user=request.user)

    form = PFPForm(request.POST, request.FILES, instance=pfp)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile picture has been set successfully!')
    else:
        """sends back any validation errors that occurred"""
        for error_msg in form.errors.as_data()['image'][0]:
            full_message = "{}".format(error_msg)
            messages.error(request, full_message)
    return redirect('chat:home')


'''Home view class. User can see and change his profile data on this page'''


class HomeView(TemplateView):
    template_name = 'chat/home.html'
    extra_context = {
        'pfp_form': PFPForm,
    }


'''User profile view class'''


class UserProfileView(View):
    template_name = 'chat/profile.html'

    def get(self, request, *args, **kwargs):
        context: Dict[str, Any] = {
            'requested_user': None,
            'pfp_form': None
        }

        requested_user = None
        if 'pk' in kwargs:
            requested_user = User.objects.get(pk=kwargs['pk'])
        elif 'username' in kwargs:
            requested_user = User.objects.get(username=kwargs['username'])
        elif request.user.is_authenticated:
            requested_user = User.objects.get(pk=request.user.pk)

        if requested_user is None:
            messages.error(request, 'You have to be authenticated or enter a valid username or id of the user')
            return redirect('chat:login')

        # if the user is authenticated and is the same as the requested user he can change his profile picture
        if requested_user == request.user:
            context['pfp_form'] = PFPForm()

        context['requested_user'] = requested_user
        return render(request, self.template_name, context=context)


'''
Chat group view class and methods
'''


def lazy_messages(request, group_id: int):
    chat_group = get_object_or_404(ChatGroup, id=group_id)
    chat_messages = reversed(chat_group.chat_messages.all()[:30])

    return render(request, 'group_messages.html', {'chat_messages': chat_messages})

class ChatGroupListView(ListView):
    model = ChatGroup
    template_name = 'chat/chat_group_list.html'
    context_object_name = 'chat_groups'

    def get_queryset(self):
        return ChatGroup.objects.all()[:30]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_groups'] = self.get_queryset()
        return context

class ChatGroupView(LoginRequiredMixin, View):
    template_name = 'chat/chat_group.html'

    login_url = reverse_lazy('chat:login')

    """
    The view can be accessed by either primary key or name of the group
    """

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if 'pk' in kwargs:
            chat_group = get_object_or_404(ChatGroup, pk=kwargs['pk'])
        elif 'group_name' in kwargs:
            chat_group = get_object_or_404(ChatGroup, name=kwargs['group_name'])
        else:
            return HttpResponse('Group not found', status=404)

        chat_messages = reversed(chat_group.chat_messages.all()[:30])

        return render(request, self.template_name, {'group': chat_group, 'chat_messages': chat_messages})

    def handle_no_permission(self):
        messages.warning(self.request, "You need to log in to access this page.")
        return redirect(f"{self.login_url}?next={self.request.get_full_path()}")
