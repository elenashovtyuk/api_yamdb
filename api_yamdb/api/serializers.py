from rest_framework import serializers

from users.models import User


class SendCodeSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    # username = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Username can not be me'
            )
        return value


class CheckConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
        # username = serializers.RegexField(
        #     r'^[\w.@+-]+\Z',
        #     max_length=150,
        #     required=True,
        #     validators=[
        #         validators.UniqueValidator(
        #             queryset=User.objects.all(),
        #             message='Пользователь с таким именем уже существует.'
        #         )
        #     ]
        # )

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role',)
        model = User
