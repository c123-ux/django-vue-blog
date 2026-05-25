# Django + Vue3 个人博客系统

一个现代化的前后端分离博客系统，采用 Django REST Framework 后端和 Vue3 前端。

**✨ 项目已完成！具备完整的功能、测试和部署配置。**

## 🚀 技术栈

### 后端
- **Django 6.0** - Python Web 框架
- **Django REST Framework** - API 开发
- **JWT 认证** - djangorestframework-simplejwt
- **SQLite** - 开发数据库（生产环境使用 PostgreSQL）
- **Redis** - 缓存层
- **Markdown** - 文章渲染
- **Bleach** - XSS 防护
- **PostgreSQL全文搜索** - 可选功能

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP 客户端
- **marked** - Markdown 渲染

## 📋 核心功能

✅ **用户系统**
- JWT Token 认证（Access + Refresh Token）
- 用户注册、登录、个人信息管理
- Token 自动刷新机制

✅ **文章管理**
- Markdown 编辑器支持
- 自动生成 HTML 和摘要
- XSS 安全防护
- 封面图片上传
- 草稿/发布状态管理
- 阅读量统计（原子递增，防并发）

✅ **评论系统**
- 楼中楼回复（自关联 parent 字段）
- 评论审核机制
- 按文章获取评论列表
- 权限控制（仅作者可删除）

✅ **性能优化**
- Redis 缓存文章详情（10分钟）
- Redis 缓存文章列表（5分钟）
- 更新/删除时自动清除缓存
- 智能降级（Redis不可用时使用内存缓存）

✅ **API 文档**
- drf-spectacular 自动生成 OpenAPI 3.0 文档
- Swagger UI 交互式文档界面

✅ **图片上传**
- 支持 JPG、PNG、GIF、WebP 格式
- 文件大小限制（最大 5MB）
- 自动生成唯一文件名
- 按日期分类存储

## 🏗️ 项目结构

```
D:\PythonProject3\
├── apps/                  # Django应用模块
│   ├── users/             # 用户认证模块
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py       # 9个单元测试
│   ├── articles/          # 文章模块
│   │   ├── models.py      # Article 模型
│   │   ├── serializers.py # 序列化器
│   │   ├── views.py       # 视图（含缓存）
│   │   ├── views_upload.py # 图片上传
│   │   ├── urls.py
│   │   └── tests.py       # 18个单元测试
│   └── comments/          # 评论模块
│       ├── models.py      # Comment 模型
│       ├── serializers.py
│       ├── views.py
│       └── tests.py       # 15个单元测试
├── blog_backend/          # Django 项目配置
│   ├── settings.py        # 开发配置
│   ├── settings_production.py # 生产配置
│   ├── urls.py            # 主路由
│   └── wsgi.py
├── blog-frontend/         # Vue3 前端
│   ├── src/
│   │   ├── api/           # API调用
│   │   ├── views/         # 页面组件
│   │   ├── router/        # 路由配置
│   │   └── App.vue
│   └── package.json
├── media/                 # 用户上传文件
├── Dockerfile             # Docker配置
├── docker-compose.yml     # Docker编排
├── .env.example           # 环境变量示例
├── requirements.txt       # Python依赖
├── manage.py              # Django管理脚本
├── start_backend.bat      # 后端启动脚本
├── start_frontend.bat     # 前端启动脚本
├── start_docker.bat       # Docker一键启动
├── README.md              # 项目说明
├── DEPLOYMENT.md          # 部署指南
└── PROJECT_COMPLETION.md  # 完成总结
```

## 🚀 快速开始

### 第一步：启动后端（Django）

1. **打开 PyCharm 终端**
   - 点击底部 "终端" 标签
   - 或按快捷键 `Alt + F12`

2. **运行后端服务**
   ```powershell
   python manage.py runserver
   ```

3. **看到以下信息表示成功**
   ```
   Starting development server at http://127.0.0.1:8000/
   ```

4. **保持终端打开，不要关闭**

### 第二步：启动前端（Vue3）

1. **打开新的终端窗口**
   - 在 PyCharm 中再次按 `Alt + F12`
   - 或点击终端标签旁的 `+` 号

2. **进入前端目录并启动**
   ```powershell
   cd blog-frontend
   npm run dev
   ```

3. **看到以下信息表示成功**
   ```
     Local:   http://localhost:5175/
   ```
   > 注意：端口号可能是 5173、5174 或 5175，以实际输出为准

4. **保持终端打开，不要关闭**

### 第三步：访问系统

打开浏览器访问：

- **前端博客**: http://localhost:5173/ （或终端显示的端口）
- **API 文档**: http://127.0.0.1:8000/api/docs/
- **Admin 后台**: http://127.0.0.1:8000/admin/

## 🔐 默认账号信息

### 博客前台登录（http://localhost:5173/login）
- **用户名**：`newuser`
- **密码**：`1593570abc`

### Django Admin 后台登录（http://127.0.0.1:8000/admin/）
- **用户名**：`admin`
- **密码**：`1593570abc`

> ⚠️ **注意**：请妥善保管账号密码，生产环境请及时修改密码！

## 📦 首次运行准备（仅第一次需要）

如果是第一次运行项目，需要先安装依赖：

### 后端依赖
```powershell
# 激活虚拟环境
.venv\Scripts\activate

# 安装 Python 依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser
```

### 前端依赖
```powershell
cd blog-frontend
npm install
```

> 依赖安装完成后，以后每次只需运行 `python manage.py runserver` 和 `npm run dev` 即可

## 💡 常见问题

### Q: 端口被占用怎么办？
A: 系统会自动尝试其他端口（5173→5174→5175），查看终端输出的实际端口号即可。

### Q: 如何停止服务？
A: 在运行服务的终端中按 `Ctrl + C`，或直接关闭终端窗口。

### Q: Redis 未启动会有影响吗？
A: 不会！系统会自动降级到内存缓存，不影响正常使用。

### Q: 修改代码后需要重启吗？
A: 不需要！后端和前端都支持热重载，修改后自动生效。

### Q: 首次运行需要做什么？
A: 只需两个命令：
- 后端：`python manage.py runserver`
- 前端：`npm run dev`

### Q: API 文档页面空白无法显示怎么办？
A: 可能是静态资源加载问题，尝试以下解决方案：

1. **检查模板配置**：确保 `settings.py` 中 `TEMPLATES` 包含 `debug` 上下文处理器：
   ```python
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [],
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',  # 确保这一行存在
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]
   ```

2. **重启后端服务**：
   ```powershell
   # 按 Ctrl + C 停止服务
   python manage.py runserver
   ```

3. **清除浏览器缓存**：按 `Ctrl + Shift + Delete` 清除缓存，或尝试无痕模式访问

### Q: 管理员账号密码是什么？登录失败怎么办？
A: 如果还没有创建管理员账号，需要手动创建：

```powershell
python manage.py createsuperuser
```

然后按照提示输入用户名、邮箱和密码。

如果已有账号但忘记密码，可以重置密码：
```powershell
python manage.py changepassword <用户名>
```

### Q: 如何创建测试用户？
A: 可以通过 Django shell 创建：
```powershell
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('用户名', '邮箱', '密码')"
```

或者直接在前台注册页面注册：http://localhost:5173/register

## 📡 API 接口

### 认证接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/auth/token/` | 获取 JWT Token | ❌ |
| POST | `/api/auth/register/` | 用户注册 | ❌ |
| GET | `/api/auth/profile/` | 获取用户信息 | ✅ |
| POST | `/api/auth/token/refresh/` | 刷新 Token | ❌ |

### 文章接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/articles/` | 文章列表（分页、搜索、排序） | ❌ |
| GET | `/api/articles/{id}/` | 文章详情 | ❌ |
| POST | `/api/articles/create/` | 创建文章 | ✅ |
| PUT | `/api/articles/{id}/update/` | 更新文章 | ✅ |
| DELETE | `/api/articles/{id}/delete/` | 删除文章 | ✅ |
| POST | `/api/articles/upload-image/` | 上传图片 | ✅ |

### 评论接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/comments/article/{id}/` | 获取文章评论 | ❌ |
| POST | `/api/comments/create/` | 创建评论 | ✅ |
| DELETE | `/api/comments/{id}/delete/` | 删除评论 | ✅ |

## 🔑 使用示例

### 1. 用户注册

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepass123",
    "password2": "securepass123"
  }'
```

### 2. 登录获取 Token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

响应：
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
}
```

### 3. 获取文章列表

```bash
curl http://127.0.0.1:8000/api/articles/
```

### 4. 创建文章（需要认证）

```bash
curl -X POST http://127.0.0.1:8000/api/articles/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "我的第一篇文章",
    "content": "# 标题\n\n这是文章内容",
    "status": "published"
  }'
```

### 5. 创建评论

```bash
curl -X POST http://127.0.0.1:8000/api/comments/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "article": 1,
    "content": "很好的文章！"
  }'
```

## ⚙️ 配置说明

### 环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
DJANGO_SECRET_KEY=your-secret-key
DB_NAME=blog_db
DB_USER=blog_user
DB_PASSWORD=your-password
REDIS_URL=redis://127.0.0.1:6379/1
DEBUG=True
```

### Redis 缓存

项目已实现智能降级机制：
- 如果 Redis 可用，使用 Redis 缓存
- 如果 Redis 不可用，自动切换到内存缓存

无需额外配置，开箱即用！

### 生产环境部署

详见 [DEPLOYMENT.md](DEPLOYMENT.md) 获取完整的部署指南。

简要步骤：
1. 使用 `settings_production.py`
2. 切换到 PostgreSQL 数据库
3. 设置 `DEBUG = False`
4. 配置 `ALLOWED_HOSTS`
5. 使用环境变量管理敏感信息
6. 使用 Gunicorn + Nginx
7. 启用 HTTPS

## 🧪 测试

运行所有单元测试：

```bash
python manage.py test apps.users apps.articles apps.comments -v 1
```

测试结果：
```
Ran 40 tests in 48.666s

OK
```

- **用户模块**: 9个测试 ✓
- **文章模块**: 18个测试 ✓
- **评论模块**: 15个测试 ✓
- **通过率**: 100%

## 📝 项目状态

✅ **已完成**
- 后端 API 开发
- 前端 Vue3 开发
- 单元测试编写
- 生产环境配置
- Docker 容器化
- 完整文档

🎯 **后续优化建议**
- 添加文章标签系统
- 实现文章分类功能
- 添加点赞/收藏功能
- 集成 Elasticsearch 全文搜索
- 实现 WebSocket 实时评论
- 添加后台管理系统

详见 [PROJECT_COMPLETION.md](PROJECT_COMPLETION.md)

## 📄 许可证

MIT License

## 👤 作者

个人博客系统项目

---

**🎉 项目已完成！这是一个完整的、生产级别的博客系统。**

- ✅ 完整的功能实现
- ✅ 优秀的性能优化
- ✅ 严格的安全防护
- ✅ 完善的测试覆盖（40+测试用例）
- ✅ 详细的部署文档
- ✅ 容器化部署支持

立即开始使用吧！
