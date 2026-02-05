<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { apiBaseUrl } from '@/config/site'
import { formatDate } from '@/lib/formatDate'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationFirst,
  PaginationLast,
  PaginationNext,
  PaginationPrevious,
  PaginationItem,
} from '@/components/ui/pagination'

const { t, locale } = useI18n()

interface Post {
  id: number
  title: string
  date: string
  excerpt: string
  tags: string[]
}

const posts = ref<Post[]>([])
const totalPosts = ref(0) // Get from backend
const currentPage = ref(1)
const postsPerPage = 12
const isLoading = ref(true)

const fetchPosts = async () => {
  isLoading.value = true
  try {
    const response = await axios.get(`${apiBaseUrl}/api/v1/blog`, {
      params: {
        page: currentPage.value,
        size: postsPerPage
      }
    })
    // 注意：依家要攞 response.data.items 同 .total
    posts.value = response.data.items
    totalPosts.value = response.data.total
  } catch (error) {
    console.error('Fetch posts error:', error)
  } finally {
    isLoading.value = false
  }
}

// 當 currentPage 改變時，重新去後端攞數
const handlePageChange = (newPage: number) => {
  currentPage.value = newPage
  fetchPosts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <div class="container max-w-5xl py-24 px-4 md:px-8">
    <div class="mb-12">
      <h1 class="text-4xl font-bold tracking-tight mb-4">{{ t('blog.title') }}</h1>
      <p class="text-muted-foreground">{{ t('blog.description') }}</p>
    </div>

    <div v-if="isLoading" class="grid gap-6 sm:grid-cols-2">
      <Card v-for="i in posts.length" :key="i" class="animate-pulse h-[200px] bg-muted/50"></Card>
    </div>

    <div v-else-if="posts.length > 0">
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-2 mb-10">
        <router-link v-for="post in posts" :key="post.id" :to="{ name: 'post-detail', params: { id: post.id } }">
          <Card class="flex flex-col h-full hover:border-zinc-500/50 transition-all">
            <CardHeader>
              <div class="flex justify-between text-xs text-muted-foreground mb-2">
                <span>{{ post.tags?.[0] }}</span>
                <time>{{ formatDate(post.date, locale) }}</time>
              </div>
              <CardTitle class="line-clamp-2">{{ post.title }}</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-muted-foreground line-clamp-2">{{ post.excerpt || '...' }}</p>
            </CardContent>
          </Card>
        </router-link>
      </div>

      <div class="flex justify-center mt-12">
        <Pagination 
          :total="totalPosts" 
          :sibling-count="1" 
          show-edges 
          :default-page="1"
          :items-per-page="postsPerPage"
          @update:page="handlePageChange"
        >
          <PaginationContent v-slot="{ items }" class="flex items-center gap-1">
            <PaginationFirst />
            <PaginationPrevious />
            <template v-for="(item, index) in items">
              <PaginationItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
                <Button class="w-10 h-10 p-0" :variant="item.value === currentPage ? 'default' : 'outline'">
                  {{ item.value }}
                </Button>
              </PaginationItem>
              <PaginationEllipsis v-else :key="item.type" :index="index" />
            </template>
            <PaginationNext />
            <PaginationLast />
          </PaginationContent>
        </Pagination>
      </div>
    </div>

  </div>
</template>