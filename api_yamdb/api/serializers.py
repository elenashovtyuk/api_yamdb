from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comment


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов (только для редактирования)."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review


class ReviewSerializer(ReviewUpdateSerializer):
    """Сериализатор для отзывов (кроме редактирования)."""

    def validate(self, data):
        request = self.context['request']
        author_id = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
            author=author_id, title=title_id
        ).exists():
            raise serializers.ValidationError(
                'Every person can add only the one review '
                'for every title'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
