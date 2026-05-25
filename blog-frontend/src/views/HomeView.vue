<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getArticles } from '@/api/article'

const router = useRouter()
const articles = ref([])
const loading = ref(true)
const pagination = ref({
  count: 0,
  next: null,
  previous: null,
})

// 加载文章列表
const loadArticles = async (page = 1) => {
  try {
    loading.value = true
    const response = await getArticles({ page })
    articles.value = response.data.results
    pagination.value = {
      count: response.data.count,
      next: response.data.next,
      previous: response.data.previous,
    }
  } catch (error) {
    console.error('Failed to load articles:', error)
  } finally {
    loading.value = false
  }
}

// 格式化日期
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 跳转到文章详情
const goToArticle = (id) => {
  router.push(`/article/${id}`)
}

// 下一页
const nextPage = () => {
  if (pagination.value.next) {
    const url = new URL(pagination.value.next)
    const page = url.searchParams.get('page')
    loadArticles(page)
  }
}

// 上一页
const prevPage = () => {
  if (pagination.value.previous) {
    const url = new URL(pagination.value.previous)
    const page = url.searchParams.get('page')
    loadArticles(page)
  }
}

onMounted(() => {
  loadArticles()
})
</script>

<template>
  <div class="home">
    <div class="container">
      <h1 class="page-title">最新文章</h1>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">加载中...</div>
      
      <!-- 文章列表 -->
      <div v-else-if="articles.length > 0" class="article-list">
        <div
          v-for="article in articles"
          :key="article.id"
          class="article-card"
          @click="goToArticle(article.id)"
        >
          <div v-if="article.cover" class="article-cover">
            <img :src="article.cover" :alt="article.title" />
          </div>
          <div class="article-content">
            <h2 class="article-title">{{ article.title }}</h2>
            <p class="article-summary">{{ article.summary }}</p>
            <div class="article-meta">
              <span class="author">👤 {{ article.author_name }}</span>
              <span class="date">📅 {{ formatDate(article.created_at) }}</span>
              <span class="views">👁️ {{ article.views }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-else class="empty-state">
        <p>暂无文章</p>
      </div>
      
      <!-- 分页 -->
      <div v-if="articles.length > 0" class="pagination">
        <button
          @click="prevPage"
          :disabled="!pagination.previous"
          class="btn-page"
        >
          上一页
        </button>
        <span class="page-info">
          共 {{ pagination.count }} 篇文章
        </span>
        <button
          @click="nextPage"
          :disabled="!pagination.next"
          class="btn-page"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.2rem;
}

.article-list {
  display: grid;
  gap: 1.5rem;
}

.article-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.article-cover {
  height: 200px;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-content {
  padding: 1.5rem;
}

.article-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.article-summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  gap: 1.5rem;
  color: #999;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 2rem;
  padding: 1rem;
}

.btn-page {
  padding: 0.5rem 1.5rem;
  border: 1px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-page:hover:not(:disabled) {
  background: #667eea;
  color: white;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
}
</style>
