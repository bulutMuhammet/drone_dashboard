# Kullanıcı kaydı için serializer
from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]

class UserRegisterSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=False)

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'team')

    def create(self, validated_data):
        team = validated_data.pop('team', None)  # Team bilgisini al ve validated_data'dan çıkar
        user = User(username=validated_data['email'], **validated_data)
        user.set_password(validated_data['password'])         # Şifreyi hashle

        user.save()

        user.staff.team = team
        user.staff.save()
        return user


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
