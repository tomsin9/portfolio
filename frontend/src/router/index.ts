import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BlogView from '../views/BlogView.vue'
import PostDetail from '../views/PostDetail.vue'

const routes = [
    { path: '/', name: 'home', component: HomeView },
    { path: '/blog', name: 'post-list', component: BlogView },
    { path: '/blog/post/:id', name: 'post-detail', component: PostDetail, props: true }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return { top: 0 }
    }
})

export default router