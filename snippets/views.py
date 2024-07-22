from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from snippets.models import Snippets
from django.contrib.auth.models import User
from snippets.serializers import SnippetsSerializer, UserSerializer
from rest_framework import renderers
from rest_framework import viewsets
    
class SnippetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Snippets.objects.all()
    serializer_class = SnippetsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderers_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
# Automatically provides 'list' and 'retrieve' actions.    
class UserViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = User.objects.all()
    serializer_class = UserSerializer

# using reverse to generate a URL for user-list & snippet-list
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
