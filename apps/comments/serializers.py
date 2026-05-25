from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment


class UserSimpleSerializer(serializers.ModelSerializer):
    """简化用户信息"""
    class Meta:
        model = User
        fields = ('id', 'username')


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'parent', 'content',
            'author_name', 'is_approved',
            'replies_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'is_approved']
    
    def get_replies_count(self, obj):
        return obj.replies.count()
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        
        # 默认审核通过（可根据需要改为需要审核）
        validated_data['is_approved'] = True
        
        return super().create(validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """评论创建序列化器"""
    class Meta:
        model = Comment
        fields = ['article', 'parent', 'content']
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("评论内容不能为空")
        if len(value) > 1000:
            raise serializers.ValidationError("评论内容不能超过1000字")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        
        # 默认审核通过
        validated_data['is_approved'] = True
        
        return super().create(validated_data)
