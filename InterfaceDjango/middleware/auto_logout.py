from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                current_session = Session.objects.get(session_key=request.session.session_key)
                current_time = datetime.datetime.now(datetime.timezone.utc)
                if current_session.expire_date <= current_time:
                    logout(request)
                    return HttpResponseRedirect(
                        reverse(
                            'users_app:user-login'
                        )
                    )
            except ObjectDoesNotExist:
                # Si la sesión no existe, simplemente continúa con la solicitud
                pass

        response = self.get_response(request)
        return response
