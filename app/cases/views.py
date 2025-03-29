from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import View, DetailView
from django.shortcuts import render
from django.http import HttpResponse

from .models import UserStatistic


class UserStatisticsView(View):
    template_name = 'cases/user_stats.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if 'pk' in kwargs:
            user_stats = get_object_or_404(UserStatistic, user__pk=kwargs['pk'])
            return render(request, self.template_name, {'user_stats': user_stats})
        elif 'username' in kwargs:
            user_stats = get_object_or_404(UserStatistic, user__username=kwargs['username'])
            return render(request, self.template_name, {'user_stats': user_stats})
        elif request.user.is_authenticated:
            user_stats = get_object_or_404(UserStatistic, user=request.user)
            return render(request, self.template_name, {'user_stats': user_stats})

        return HttpResponse('User not found', status=404)
