from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password", "confirm_password"]
        lookup_field = 'username'

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm_Password doesn't match.")
        return attrs

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('user with this username already exists.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        user.save()
        return user


# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'first_name', 'last_name')
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data.get('username'),
#             first_name=validated_data.get('first_name'),
#             last_name=validated_data.get('last_name')
#         )
#
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user
