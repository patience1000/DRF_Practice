from django.urls import path
from snippets import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import renderers
from snippets.views import api_root, SnippetsViewSet, UserViewSet
from rest_framework.urlpatterns import format_suffix_patterns
# creating our routers to register our viewsets

snippet_list = SnippetsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetsViewSet.as_view({
    'get': 'retrive',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetsViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/',snippet_highlight,name='snippet-highlight'),
    path('users/',user_list,name='user-list'),
    path('users/<int:pk>/',user_detail,name='user-detail')
])
router = DefaultRouter()
router.register(r'snippets', views.SnippetsViewSet, basename='snippets')
router.register(r'users', views.UserViewSet, basename='user')


