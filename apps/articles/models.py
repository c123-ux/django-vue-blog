from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils.text import slugify
import markdown
import bleach
import uuid

# 尝试导入 PostgreSQL 搜索功能（可选）
try:
    from django.contrib.postgres.search import SearchVectorField, SearchVector
    HAS_POSTGRES_SEARCH = True
except ImportError:
    HAS_POSTGRES_SEARCH = False
    # 如果不支持 PostgreSQL，使用普通 TextField
    class SearchVectorField(models.TextField):
        def __init__(self, *args, **kwargs):
            kwargs['null'] = True
            kwargs['blank'] = True
            super().__init__(*args, **kwargs)


class Article(models.Model):
    """文章模型"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('slug', max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, verbose_name='作者', related_name='articles', on_delete=models.CASCADE)
    content = models.TextField('Markdown内容')
    content_html = models.TextField('HTML内容', blank=True, editable=False)
    summary = models.TextField('摘要', blank=True)
    cover = models.ImageField('封面图片', upload_to='article_covers/%Y/%m/', blank=True, null=True)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField('阅读量', default=0)
    search_vector = SearchVectorField('搜索向量', null=True, blank=True)  # PostgreSQL 全文搜索
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 自动生成 slug
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
            self.slug = unique_slug
        
        # Markdown 渲染 + XSS 防护
        if self.content:
            html_content = markdown.markdown(
                self.content,
                extensions=['extra', 'codehilite', 'toc']
            )
            # 使用 bleach 清理 HTML，防止 XSS
            allowed_tags = [
                'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'strong', 'em', 'code', 'pre', 'blockquote',
                'ul', 'ol', 'li', 'a', 'img', 'table', 'thead',
                'tbody', 'tr', 'th', 'td', 'hr'
            ]
            allowed_attrs = {
                'a': ['href', 'title', 'target'],
                'img': ['src', 'alt', 'title'],
                'code': ['class'],
                'pre': ['class'],
            }
            self.content_html = bleach.clean(
                html_content,
                tags=allowed_tags,
                attributes=allowed_attrs,
                strip=True
            )

        # 自动生成摘要（前 200 个字符）
        if not self.summary and self.content:
            # 去除 Markdown 标记
            text_content = bleach.clean(self.content, strip=True)
            self.summary = text_content[:200] + '...' if len(text_content) > 200 else text_content

        super().save(*args, **kwargs)
        
        # 更新搜索向量（仅在使用 PostgreSQL 时）
        self.update_search_vector()
    
    def update_search_vector(self):
        """更新全文搜索向量（PostgreSQL）"""
        if not HAS_POSTGRES_SEARCH:
            return
        
        try:
            from django.db import connection
            if connection.vendor == 'postgresql':
                Article.objects.filter(pk=self.pk).update(
                    search_vector=SearchVector('title', weight='A') + 
                                   SearchVector('summary', weight='B') +
                                   SearchVector('content', weight='C')
                )
        except Exception:
            # 如果使用 SQLite 或其他数据库，忽略此功能
            pass

    def increase_views(self):
        """原子递增阅读量（防并发）"""
        Article.objects.filter(pk=self.pk).update(views=F('views') + 1)
        self.refresh_from_db()

    def get_summary(self):
        """获取摘要"""
        return self.summary
