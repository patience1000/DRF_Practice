from rest_framework import serializers
from django.contrib.auth.models import User
from snippets.models import Snippets, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight',format='html')

    class Meta:
        model = Snippets
        fields = ['id','url','highlight','title','code','linenos','language','style','owner']
        
        extra_kwargs = {
            'url': {'view_name': 'snippet-detail'}  # Ensure this matches the name in urls.py
        }

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    class Meta:
        model = User
        fields = ['url','id','username','snippets']
        