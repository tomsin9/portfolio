import { createRouter, createWebHistory } from 'vue-router'
import { trackPageView } from '@/lib/analytics'
import HomeView from '../views/HomeView.vue'
import AdminLogin from '../views/AdminLogin.vue'
import BlogView from '../views/BlogView.vue'
import PostDetail from '../views/PostDetail.vue'

const routes = [
    { path: '/', name: 'home', component: HomeView },
    { path: '/secret/login', name: 'admin-login', component: AdminLogin },
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

router.afterEach((to) => {
    trackPageView(to.fullPath)
})

export default router