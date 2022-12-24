from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comment

from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    # author = SlugRelatedField(read_only=True, slug_field='username')
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        fields = '__all__'
        model = Review
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('author', 'title')
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = SlugRelatedField(read_only=True, slug_field='name')
    review = SlugRelatedField(read_only=True, slug_field='text')

    class Meta:
        fields = '__all__'
        model = Comment
