<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getArticle } from '@/api/article'
import { getComments, createComment } from '@/api/comment'
import { marked } from 'marked'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const article = ref(null)
const comments = ref([])
const loading = ref(true)
const newComment = ref('')

// 加载文章详情
const loadArticle = async () => {
  try {
    const response = await getArticle(route.params.id)
    article.value = response.data
  } catch (error) {
    console.error('Failed to load article:', error)
  }
}

// 加载评论
const loadComments = async () => {
  try {
    const response = await getComments(route.params.id)
    comments.value = response.data
  } catch (error) {
    console.error('Failed to load comments:', error)
  }
}

// 提交评论
const submitComment = async () => {
  if (!newComment.value.trim()) return
  
  try {
    await createComment({
      article: article.value.id,
      content: newComment.value,
    })
    newComment.value = ''
    await loadComments()
  } catch (error) {
    console.error('Failed to create comment:', error)
    alert('发表评论失败')
  }
}

// 格式化日期
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(async () => {
  loading.value = true
  await Promise.all([loadArticle(), loadComments()])
  loading.value = false
})
</script>

<template>
  <div class="article-detail">
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else-if="article" class="container">
      <!-- 文章头部 -->
      <header class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <span class="author">👤 {{ article.author_name }}</span>
          <span class="date">📅 {{ formatDate(article.created_at) }}</span>
          <span class="views">👁️ {{ article.views }} 次阅读</span>
        </div>
      </header>
      
      <!-- 封面图片 -->
      <div v-if="article.cover" class="article-cover">
        <img :src="article.cover" :alt="article.title" />
      </div>
      
      <!-- 文章内容 -->
      <article class="article-content" v-html="article.content_html"></article>
      
      <!-- 评论区 -->
      <section class="comments-section">
        <h2 class="comments-title">评论 ({{ comments.length }})</h2>
        
        <!-- 发表评论 -->
        <div v-if="authStore.isAuthenticated" class="comment-form">
          <textarea
            v-model="newComment"
            placeholder="写下你的评论..."
            rows="4"
          ></textarea>
          <button @click="submitComment" class="btn-submit">发表评论</button>
        </div>
        <div v-else class="login-tip">
          <router-link to="/login">登录</router-link> 后发表评论
        </div>
        
        <!-- 评论列表 -->
        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <strong>{{ comment.author_name }}</strong>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.article-detail {
  padding: 2rem 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
}

.loading {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
}

.article-header {
  margin-bottom: 2rem;
}

.article-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.article-meta {
  display: flex;
  gap: 2rem;
  color: #999;
  font-size: 0.95rem;
}

.article-cover {
  margin-bottom: 2rem;
  border-radius: 8px;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
}

.article-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  line-height: 1.8;
  color: #333;
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3) {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.article-content :deep(p) {
  margin-bottom: 1rem;
}

.article-content :deep(code) {
  background: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.article-content :deep(pre) {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
}

.comments-section {
  margin-top: 3rem;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comments-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.comment-form {
  margin-bottom: 2rem;
}

.comment-form textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  resize: vertical;
  margin-bottom: 1rem;
}

.comment-form textarea:focus {
  outline: none;
  border-color: #667eea;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.3s;
}

.btn-submit:hover {
  transform: translateY(-2px);
}

.login-tip {
  text-align: center;
  padding: 1rem;
  color: #666;
}

.login-tip a {
  color: #667eea;
  text-decoration: none;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-date {
  color: #999;
  font-size: 0.9rem;
}

.comment-content {
  color: #555;
  line-height: 1.6;
}
</style>
