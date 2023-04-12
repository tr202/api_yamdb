from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(many=False, required=False)
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleDetailSerializer(TitleSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
    
    def get_rating(self, obj):
        rewievs = Review.objects.filter(title=obj)
        sum = 0
        count = 0
        for review in rewievs:
            sum += review.score
            count += 1
        if sum>0:
            return int(sum/count)
        else:
            return 'None'
        


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    def validate_score(self, value):
        if value > 10:
            raise serializers.ValidationError("Score can not be more than 10")
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
