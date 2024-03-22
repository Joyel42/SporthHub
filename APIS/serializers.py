from .models import Users, SportList, favSports, brodacastMessages
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

class SportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportList
        fields = "__all__"

class favSportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = favSports
        fields = "__all__"


class BrodcastMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = brodacastMessages
        fields = "__all__"