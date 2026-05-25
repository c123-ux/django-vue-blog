"""
创建测试数据的脚本
运行: python create_test_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
django.setup()

from django.contrib.auth.models import User
from apps.articles.models import Article

# 创建测试用户
if not User.objects.filter(username='testuser').exists():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    print(f"创建测试用户: {user.username}")
else:
    user = User.objects.get(username='testuser')
    print(f"测试用户已存在: {user.username}")

# 创建测试文章
test_articles = [
    {
        'title': 'Django REST Framework 完全指南',
        'content': '''# Django REST Framework 完全指南

DRF 是一个强大的 Django 扩展，用于构建 Web API。

## 主要特性

- **序列化器**: 轻松转换复杂数据
- **视图集**: 简化 CRUD 操作
- **认证与权限**: 灵活的安全控制
- **自动文档**: 内置 API 文档生成

## 安装

```bash
pip install djangorestframework
```

## 快速开始

创建一个简单的 API 只需要几行代码！
''',
        'status': 'published'
    },
    {
        'title': 'Vue3 组合式 API 最佳实践',
        'content': '''# Vue3 组合式 API 最佳实践

Vue3 引入了组合式 API，提供了更灵活的代码组织方式。

## 核心概念

### setup() 函数

```javascript
import { ref, computed } from 'vue'

export default {
  setup() {
    const count = ref(0)
    const doubleCount = computed(() => count.value * 2)
    
    return { count, doubleCount }
  }
}
```

### 响应式引用

使用 `ref` 和 `reactive` 创建响应式数据。
''',
        'status': 'published'
    },
    {
        'title': 'Python 异步编程入门',
        'content': '''# Python 异步编程入门

异步编程可以显著提高 I/O 密集型应用的性能。

## asyncio 基础

```python
import asyncio

async def main():
    print('Hello')
    await asyncio.sleep(1)
    print('World')

asyncio.run(main())
```

## 实际应用场景

- Web 爬虫
- WebSocket 服务器
- 高并发 API 服务
''',
        'status': 'draft'
    }
]

for article_data in test_articles:
    if not Article.objects.filter(title=article_data['title']).exists():
        article = Article.objects.create(
            title=article_data['title'],
            content=article_data['content'],
            author=user,
            status=article_data['status']
        )
        print(f"创建文章: {article.title}")
    else:
        print(f"文章已存在: {article_data['title']}")

print("\n测试数据创建完成！")
print(f"用户名: testuser")
print(f"密码: testpass123")
