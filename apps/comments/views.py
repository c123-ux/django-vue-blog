from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache

from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer


class CommentListView(generics.ListAPIView):
    """获取某文章的评论列表"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return Comment.objects.filter(
            article_id=article_id,
            is_approved=True,
            parent=None  # 只返回顶级评论
        ).select_related('author').order_by('-created_at')


class CommentCreateView(generics.CreateAPIView):
    """创建评论"""
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        comment = serializer.save()
        
        # 清除文章详情缓存
        cache.delete(f'article_detail:{comment.article.id}')


class CommentDeleteView(generics.DestroyAPIView):
    """删除评论（仅作者或管理员）"""
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 权限检查：只有作者可以删除
        if instance.author != request.user and not request.user.is_staff:
            return Response(
                {'error': '无权删除此评论'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        article_id = instance.article.id
        self.perform_destroy(instance)
        
        # 清除缓存
        cache.delete(f'article_detail:{article_id}')
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
