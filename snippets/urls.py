from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view(), name="snippets_get_post"),
    url(
        r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(),
        name="snippets_get_put_delete"
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
