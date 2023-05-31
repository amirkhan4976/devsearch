from rest_framework import serializers
from testapp.models import Projects, Tags, Reviews
from users.models import Profile


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class ProjectsSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagsSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = "__all__"

    def get_reviews(self, obj):
        reviews = obj.reviews_set.all()
        serialized = ReviewsSerializer(instance=reviews, many=True)
        return serialized.data
