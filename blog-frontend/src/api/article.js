import api from './index'

// 获取文章列表
export function getArticles(params = {}) {
  return api.get('/articles/', { params })
}

// 获取文章详情
export function getArticle(id) {
  return api.get(`/articles/${id}/`)
}

// 创建文章
export function createArticle(data) {
  return api.post('/articles/create/', data)
}

// 更新文章
export function updateArticle(id, data) {
  return api.put(`/articles/${id}/update/`, data)
}

// 删除文章
export function deleteArticle(id) {
  return api.delete(`/articles/${id}/delete/`)
}

// 上传图片
export function uploadImage(file) {
  const formData = new FormData()
  formData.append('image', file)
  return api.post('/articles/upload-image/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}
