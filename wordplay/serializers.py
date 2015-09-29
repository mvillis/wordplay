from wordplay.responses.models import Response
from rest_framework import serializers


class ResponseSerializer(serializers.ModelSerializer):
    class meta:
        model = Response
        fields = 'word'


