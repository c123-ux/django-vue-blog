from django.core.cache import cache
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Article, HAS_POSTGRES_SEARCH
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleCreateSerializer
)


class ArticleListView(generics.ListAPIView):
    """文章列表视图（支持分页、搜索、过滤）"""
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'summary']  # 简单搜索
    ordering_fields = ['created_at', 'views']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        # 如果使用 PostgreSQL，启用全文搜索
        if HAS_POSTGRES_SEARCH and search_query:
            try:
                from django.db import connection
                from django.contrib.postgres.search import SearchQuery, SearchRank
                
                if connection.vendor == 'postgresql':
                    # 使用 PostgreSQL 全文搜索
                    search_vector = 'search_vector'
                    query = SearchQuery(search_query)
                    queryset = queryset.annotate(
                        rank=SearchRank(search_vector, query)
                    ).filter(
                        search_vector=query
                    ).order_by('-rank')
            except Exception:
                # 如果出错，回退到默认搜索
                pass
        
        return queryset

    def list(self, request, *args, **kwargs):
        # 尝试从缓存获取
        cache_key = f'article_list:{request.query_params}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        # 缓存未命中，查询数据库
        response = super().list(request, *args, **kwargs)
        
        # 写入缓存（5分钟）
        cache.set(cache_key, response.data, 300)
        
        return response


class ArticleDetailView(generics.RetrieveAPIView):
    """文章详情视图"""
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 原子递增阅读量
        instance.increase_views()
        
        # 尝试从缓存获取
        cache_key = f'article_detail:{instance.id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        # 缓存未命中，序列化数据
        serializer = self.get_serializer(instance)
        
        # 写入缓存（10分钟）
        cache.set(cache_key, serializer.data, 600)
        
        return Response(serializer.data)


class ArticleCreateView(generics.CreateAPIView):
    """创建文章视图"""
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleUpdateView(generics.UpdateAPIView):
    """更新文章视图"""
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # 清除缓存
        cache.delete(f'article_detail:{self.get_object().id}')
        # 简单方式：清除所有以 article_list: 开头的缓存
        cache.clear()  # 或者使用更精细的缓存键管理
        serializer.save()


class ArticleDeleteView(generics.DestroyAPIView):
    """删除文章视图"""
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # 清除缓存
        cache.delete(f'article_detail:{instance.id}')
        cache.clear()  # 清除所有缓存
        instance.delete()
