from django.conf.urls import include, url
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
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls'))
]
urlpatterns = format_suffix_patterns(urlpatterns)
