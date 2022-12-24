from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comment

from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        # Понадобится ли CurrentDefaultUser() тоже станет известно
        # после появления авторизации. Пока не мешает
        default=serializers.CurrentUserDefault()
    )
    # Это тоже пробная заготовка под валидацию, может и не понадобится
    # title = serializers.HiddenField(read_only=True, default=)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review

        #  ТУДУ: Валидатор наверняка понадобится, чтобы ограничить
        #  количество отзывов от одного человека на одно произведение,
        #  но пока недоразобралась, как это сделать. Возможно, нужен
        #  кастомный валидатор. Если делать так, как написано ниже,
        #  то появляется ошибка, что неизвестно, что такое 'title' в
        #  fields
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('title', 'author'),
        #         message=(
        #             'Every title must have only the one review '
        #             'from one person'
        #         )
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        # Понадобится ли CurrentDefaultUser() тоже станет известно
        # после появления авторизации. Пока не мешает
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
