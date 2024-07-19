from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from snippets.models import Snippets
from django.contrib.auth.models import User
from snippets.serializers import SnippetsSerializer, UserSerializer
from rest_framework import generics
from rest_framework import renderers

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippets.objects.all()
    serializer_class = SnippetsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippets.objects.all()
    serializer_class = SnippetsSerializer    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer    

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippets.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]
    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
     
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
