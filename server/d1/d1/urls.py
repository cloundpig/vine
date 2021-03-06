from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from d1.views import *
from vine_comment.views import *

# NORMAL url patterns
urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^matrix/?$', TemplateView.as_view(template_name='matrix/matrix.html'), name='matrix'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url('', include('social.apps.django_app.urls', namespace='social')),
)

# TEST python-social-auth
urlpatterns = patterns('',
    url(r'^$', 'social_auth_app.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup-email/', 'social_auth_app.views.signup_email'),
    url(r'^email-sent/', 'social_auth_app.views.validation_sent'),
    url(r'^login/$', 'social_auth_app.views.home'),
    url(r'^logout/$', 'social_auth_app.views.logout'),
    url(r'^done/$', 'social_auth_app.views.done', name='done'),
    url(r'^email/$', 'social_auth_app.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
)

urlpatterns += patterns('',
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^comment/(?P<url_b64>.*?)/?$', CommentView.as_view(), name='comment'),
    url(r'^ajax/comment/(?P<url_b64>.*?)/?$', CommentRawView.as_view(), name='comment_raw'),
    url(r'^comment_raw/(?P<url_b64>.*?)/?$', CommentRawView.as_view(), name='comment_raw'),
    url(r'^account/(?P<url_b64>.*?)/?$', AccountView.as_view(), name='account'),
    url(r'^account_raw/(?P<url_b64>.*?)/?$', AccountRawView.as_view(), name='account_raw'),
    url(r'^letter/(?P<url_b64>.*?)/?$', LetterView.as_view(), name='letter'),
    url(r'^letter_raw/(?P<url_b64>.*?)/?$', LetterRawView.as_view(), name='letter_raw'),
    url(r'^setting/(?P<url_b64>.*?)/?$', SettingView.as_view(), name='setting'),
    url(r'^setting_raw/(?P<url_b64>.*?)/?$', SettingRawView.as_view(), name='setting_raw'),
    url(r'^test/$', TemplateView.as_view(template_name='social_signin.html'), name='test'),
)

from functools import wraps
from django.contrib.staticfiles.views import serve as serve_static

if settings.DEBUG:

    def custom_headers(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            response['Access-Control-Allow-Origin'] = '*'
            return response

        return wrapper

    urlpatterns += patterns('',
        url(r'iframe/(?P<url_b64>.*?)/?$', custom_headers(CommentIframeView.as_view()), name='comment_iframe'),
        url(r'^static/(?P<path>.*)$', custom_headers(serve_static)),
    )
    