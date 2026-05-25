# Blog Frontend - Vue3 前端

基于 Vue3 + Vite + Pinia 的博客前端项目。

## 🚀 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Pinia** - Vue 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP 客户端
- **Marked** - Markdown 解析器

## 📁 项目结构

```
blog-frontend/
├── src/
│   ├── api/              # API 调用封装
│   │   ├── index.js      # Axios 实例和拦截器
│   │   ├── article.js    # 文章相关 API
│   │   └── comment.js    # 评论相关 API
│   ├── stores/           # Pinia 状态管理
│   │   └── auth.js       # 用户认证状态
│   ├── router/           # 路由配置
│   │   └── index.js
│   ├── views/            # 页面组件
│   │   ├── HomeView.vue       # 首页（文章列表）
│   │   ├── ArticleView.vue    # 文章详情
│   │   ├── LoginView.vue      # 登录页
│   │   ├── RegisterView.vue   # 注册页
│   │   └── EditorView.vue     # 文章编辑器
│   ├── App.vue           # 根组件（含导航栏）
│   ├── main.js           # 入口文件
│   └── style.css         # 全局样式
├── vite.config.js        # Vite 配置
├── package.json
└── README.md
```

## 🛠️ 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问：http://localhost:5173

### 3. 构建生产版本

```bash
npm run build
```

## 🔑 核心功能

### ✅ 已完成

- [x] 用户登录/注册
- [x] JWT Token 自动管理（含刷新）
- [x] 文章列表（分页）
- [x] 文章详情（Markdown 渲染）
- [x] 文章创建/编辑
- [x] 评论系统
- [x] 路由守卫（需登录页面保护）
- [x] 响应式设计

### 🎨 UI 特性

- 渐变紫色主题
- 卡片式布局
- 平滑过渡动画
- 优雅的加载状态

## 📡 API 代理配置

在 `vite.config.js` 中配置了 API 代理：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    }
  }
}
```

所有 `/api` 开头的请求会自动转发到 Django 后端。

## 🔐 认证流程

1. 用户登录 → 获取 Access Token + Refresh Token
2. Token 存储在 localStorage
3. Axios 拦截器自动添加 Authorization header
4. Token 过期时自动刷新
5. 刷新失败则跳转登录页

## 🎯 路由说明

| 路径 | 组件 | 需要登录 | 说明 |
|------|------|----------|------|
| `/` | HomeView | ❌ | 首页（文章列表） |
| `/article/:id` | ArticleView | ❌ | 文章详情 |
| `/login` | LoginView | ❌ | 登录页 |
| `/register` | RegisterView | ❌ | 注册页 |
| `/editor` | EditorView | ✅ | 创建文章 |
| `/editor/:id` | EditorView | ✅ | 编辑文章 |

## 💡 开发提示

### 添加新页面

1. 在 `src/views/` 创建组件
2. 在 `src/router/index.js` 添加路由
3. 如需登录保护，添加 `meta: { requiresAuth: true }`

### 调用 API

```javascript
import { getArticles } from '@/api/article'

const loadArticles = async () => {
  const response = await getArticles({ page: 1 })
  console.log(response.data)
}
```

### 使用状态管理

```javascript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
console.log(authStore.isAuthenticated)
```

## 🌐 浏览器支持

- Chrome (最新)
- Firefox (最新)
- Safari (最新)
- Edge (最新)

## 📝 注意事项

1. **后端必须先运行**：确保 Django 后端在 http://127.0.0.1:8000 运行
2. **CORS 已配置**：后端已允许前端跨域访问
3. **Markdown 支持**：文章详情页使用 marked 库渲染 Markdown

## 🚧 待完善

- [ ] 暗色模式切换
- [ ] 图片上传功能
- [ ] 文章搜索
- [ ] 标签系统
- [ ] 响应式优化（移动端）
- [ ] 错误边界处理
- [ ] 单元测试

---

**开发愉快！** 🎉
