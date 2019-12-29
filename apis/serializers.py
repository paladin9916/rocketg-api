from rest_framework import serializers

from apis.models import Images, ExpenseFile


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"


class ExpenseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseFile
        fields = "__all__"