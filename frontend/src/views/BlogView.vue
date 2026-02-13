<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { apiBaseUrl } from '@/config/site'
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import BlogCard from '@/components/BlogCard.vue'
import { useRoute, useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { auth } from '@/store/auth'
import { PlusIcon } from 'lucide-vue-next'
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

import type { Post } from '@/types/blog'

const { t } = useI18n()

const route = useRoute()
const router = useRouter()

const posts = ref<Post[]>([])
const totalPosts = ref(0) // Get from backend
const postsPerPage = 12
const isLoading = ref(true)

const currentPage = ref(Number(route.query.page) || 1)

const fetchPosts = async () => {
  isLoading.value = true
  try {
    const response = await axios.get(`${apiBaseUrl}/api/v1/blog/`, {
      params: {
        page: currentPage.value,
        size: postsPerPage
      }
    })
    // now we need to get response.data.items and response.data.total
    posts.value = response.data?.items || []
    totalPosts.value = response.data?.total || 0
  } catch (error) {
    console.error('Fetch posts error:', error)
  } finally {
    isLoading.value = false
  }
}

const handlePageChange = (newPage: number) => {
  currentPage.value = newPage
  router.push({ query: { page: newPage.toString() } })
}

watch(
  () => route.query.page,
  (newPage) => {
    currentPage.value = Number(newPage) || 1
    fetchPosts()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  },
  { immediate: true } // with this, we can skip onMounted
)

</script>

<template>
  <div class="container max-w-5xl pt-12 pb-32 lg:pt-20 lg:pb-40 px-4 md:px-8">
    <div class="text-center mb-12">
      <h2 class="text-4xl lg:text-5xl font-bold mb-6">
        {{ t('blog.title') }}
      </h2>
      <p class="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
        {{ t('blog.description') }}
      </p>
      <Button
        v-if="auth.isAdmin"
        as="a"
        :href="'/blog/post/new'"
        variant="default"
        size="sm"
        class="mt-4"
      >
        <PlusIcon class="w-4 h-4 mr-2" />
        {{ t('blog.createPost') }}
      </Button>
    </div>

    <div v-if="isLoading" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-2 mb-10">
      <Card v-for="i in posts.length" :key="i" class="flex flex-col h-full justify-between border-zinc-500/20">
        <CardHeader>
          <div class="flex justify-between items-start mb-2">
            <Skeleton class="h-5 w-16" />
            <Skeleton class="h-4 w-20" />
          </div>
          <Skeleton class="h-6 w-full mt-2" />
          <Skeleton class="h-6 w-4/5" />
        </CardHeader>
        <CardContent>
          <Skeleton class="h-4 w-full" />
          <Skeleton class="h-4 w-full mt-2" />
          <Skeleton class="h-4 w-2/3 mt-2" />
        </CardContent>
        <CardFooter>
          <Skeleton class="h-5 w-24" />
        </CardFooter>
      </Card>
    </div>

    <div v-else-if="posts.length > 0">
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-2 mb-10">
        <router-link v-for="post in posts" :key="post.id" :to="{ name: 'post-detail', params: { id: post.id }, state: { from: 'blog' } }" class="block">
          <BlogCard :post="post" />
        </router-link>
      </div>

      <div v-if="totalPosts > postsPerPage" class="flex justify-center mt-12">
        <Pagination 
          v-model:page="currentPage"
          :total="totalPosts" 
          :default-page="1"
          :sibling-count="1" 
          :items-per-page="postsPerPage"
          show-edges 
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