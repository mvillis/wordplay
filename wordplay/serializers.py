from wordplay.responses.models import Collector
from rest_framework import serializers


class CollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collector
        fields = ('open_date', 'close_date', 'survey', 'active')
