
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from main import views
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView
from main.graphql.scheme import schema
from main.graphql.view import GraphQLView as GQV
from django.conf.urls.static import static


handler404 = views.error404

urlpatterns = [
    path('admin/defender/', include('defender.urls')),
    path('grappelli/', include('grappelli.urls')),
    path("admin/", admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    # path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema, subscriptions_enabled=True)), name='graphql'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('graphql/', csrf_exempt(GQV.as_view(graphiql=True, schema=schema, subscriptions_enabled=True)), name='graphql'),
    path('rest/', include('main.rest.urls')),
    path('adminactions/', include('adminactions.urls')),
    path("", include("main.urls")),
]

urlpatterns += i18n_patterns (
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)