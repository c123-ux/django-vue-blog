"""
API 测试脚本 - 验证后端功能
运行: python test_api.py
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_register():
    """测试用户注册"""
    print("\n=== 测试用户注册 ===")
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "apitest",
        "email": "apitest@example.com",
        "password": "testpass123",
        "password2": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 201
    except Exception as e:
        print(f"错误: {e}")
        return False


def test_login():
    """测试登录获取 Token"""
    print("\n=== 测试登录 ===")
    url = f"{BASE_URL}/auth/token/"
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            tokens = response.json()
            print(f"Access Token: {tokens['access'][:50]}...")
            print(f"Refresh Token: {tokens['refresh'][:50]}...")
            return tokens['access']
        else:
            print(f"响应: {response.json()}")
            return None
    except Exception as e:
        print(f"错误: {e}")
        return None


def test_get_articles():
    """测试获取文章列表"""
    print("\n=== 测试获取文章列表 ===")
    url = f"{BASE_URL}/articles/"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"文章总数: {data.get('count', 0)}")
            if 'results' in data and len(data['results']) > 0:
                print(f"\n第一篇文章:")
                article = data['results'][0]
                print(f"  标题: {article['title']}")
                print(f"  作者: {article['author_name']}")
                print(f"  阅读量: {article['views']}")
            return True
        else:
            print(f"响应: {response.json()}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False


def test_get_article_detail(article_id=1):
    """测试获取文章详情"""
    print(f"\n=== 测试获取文章详情 (ID={article_id}) ===")
    url = f"{BASE_URL}/articles/{article_id}/"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            article = response.json()
            print(f"标题: {article['title']}")
            print(f"摘要: {article['summary'][:100]}...")
            print(f"HTML内容长度: {len(article['content_html'])} 字符")
            return True
        else:
            print(f"响应: {response.json()}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False


def test_create_article(token):
    """测试创建文章"""
    print("\n=== 测试创建文章 ===")
    url = f"{BASE_URL}/articles/create/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "API 测试文章",
        "content": "# 测试\n\n这是通过 API 创建的文章。",
        "status": "draft"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 201:
            article = response.json()
            print(f"创建成功！")
            print(f"响应数据: {json.dumps(article, indent=2, ensure_ascii=False)}")
            return article.get('id', 'N/A')
        else:
            print(f"响应: {response.json()}")
            return None
    except Exception as e:
        print(f"错误: {e}")
        return None


def test_get_comments(article_id=1):
    """测试获取评论列表"""
    print(f"\n=== 测试获取文章评论 (Article ID={article_id}) ===")
    url = f"{BASE_URL}/comments/article/{article_id}/"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            comments = response.json()
            print(f"评论数量: {len(comments)}")
            return True
        else:
            print(f"响应: {response.json()}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False


def main():
    print("=" * 60)
    print("Django 博客系统 API 测试")
    print("=" * 60)
    
    # 测试无需认证的接口
    test_get_articles()
    test_get_article_detail(1)
    
    # 测试需要认证的接口
    token = test_login()
    
    if token:
        test_create_article(token)
        test_get_comments(1)
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
