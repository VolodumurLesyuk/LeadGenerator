# from django.utils import timezone
# from django.contrib.auth import logout
# from django.contrib.sessions.middleware import SessionMiddleware
#
#
# class LastActivityMiddleware(SessionMiddleware):
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         if request.user.is_authenticated:
#             last_activity = request.session.get('last_activity')
#             if not last_activity:
#                 # Якщо значення 'last_activity' відсутнє, встановлюємо його у форматі datetime
#                 request.session['last_activity'] = timezone.now().isoformat()
#             else:
#                 # Зберігаємо значення 'last_activity' при кожному новому запиті у форматі datetime
#                 request.session['last_activity'] = timezone.now().isoformat()
#
#                 # Використовуйте last_activity для порівняння
#                 inactive_period = timezone.now() - timezone.datetime.fromisoformat(last_activity)
#
#                 if inactive_period.total_seconds() > 600:  # 10 секунд для тестування
#                     logout(request)
#
#
from django.utils import translation


class SessionLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Спочатку спробуємо отримати мову з сесії
        language = request.session.get('django_language')

        if not language:
            # Якщо мова не знайдена у сесії, шукаємо в cookies
            language = request.COOKIES.get('django_language')

        if language:
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
        else:
            # Встановлення мови за замовчуванням
            default_language = 'en'
            translation.activate(default_language)
            request.LANGUAGE_CODE = default_language

        response = self.get_response(request)

        # Зберігаємо мову у cookies
        if language:
            response.set_cookie('django_language', language)

        return response

import logging
from typing import Callable
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.messages import info

from main.django_last_activity.utils import now, seconds_until_idle_time_end, seconds_until_session_end

UserModel = get_user_model()
logger = logging.getLogger(__name__)


def _auto_logout(request: HttpRequest, options):
    should_logout = False
    current_time = now()

    if 'SESSION_TIME' in options:
        session_time = seconds_until_session_end(request, options['SESSION_TIME'], current_time)
        should_logout |= session_time < 0
        logger.debug('Check SESSION_TIME: %ss until session ends.', session_time)

    if 'IDLE_TIME' in options:
        idle_time = seconds_until_idle_time_end(request, options['IDLE_TIME'], current_time)
        should_logout |= idle_time < 0
        logger.debug('Check IDLE_TIME: %ss until idle ends.', idle_time)

        if should_logout and 'django_auto_logout_last_request' in request.session:
            del request.session['django_auto_logout_last_request']
        else:
            request.session['django_auto_logout_last_request'] = current_time.isoformat()

    if should_logout:
        logger.debug('Logout user %s', request.user)
        logout(request)

        if 'MESSAGE' in options:
            info(request, options['MESSAGE'])


def auto_logout(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable:
    def middleware(request: HttpRequest) -> HttpResponse:
        if not request.user.is_anonymous and hasattr(settings, 'AUTO_LOGOUT'):
            _auto_logout(request, settings.AUTO_LOGOUT)

        return get_response(request)
    return middleware


