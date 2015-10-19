from wordplay.responses.models import Collector
from wordplay.responses.models import Response
from rest_framework import serializers


class CollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collector
        fields = ('open_date', 'close_date', 'survey', 'active')


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('word', 'responder', 'responded_at', 'collector')
