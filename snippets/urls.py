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
    url(r'^users/$', views.UserList.as_view(), name="users_get_list"),
    url(
        r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name="snippets_get_detail"
    ),
    url(r'^$', views.api_root),
    url(
        r'^snippet/(?P<pk>[0-9]+)/highlight/$',
        views.SnippetHighlight.as_view(),
        name="snippet_highlight"
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
