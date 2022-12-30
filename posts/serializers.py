from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    
    def get_profile_image(self, obj):
        default_image = "default_profile_-_coding_gmxlr4"
        if obj.owner.profile.image:
            return obj.owner.profile.image
        else:
            return cloudinary.CloudinaryImage(default_image).build_url()

    profile_image = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.owner == request.user
        return False

    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'owner', 'is_owner', 'profile_id',
                  'profile_image', 'title', 'description']
