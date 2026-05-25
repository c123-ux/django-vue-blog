from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article


class UserSimpleSerializer(serializers.ModelSerializer):
    """简化用户信息序列化器"""
    class Meta:
        model = User
        fields = ('id', 'username')


class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化器（轻量级）"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'summary', 'cover', 'author_name',
            'views', 'created_at', 'updated_at'
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    cover = serializers.ImageField(use_url=True, required=False, allow_null=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content', 'content_html', 'summary',
            'cover', 'author_name', 'views', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['content_html', 'views']


class ArticleCreateSerializer(serializers.ModelSerializer):
    """文章创建序列化器"""
    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'cover', 'status']
    
    def create(self, validated_data):
        # 自动设置作者为当前用户
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)
