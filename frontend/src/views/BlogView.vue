<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { apiBaseUrl } from '@/config/site'
import { Card } from '@/components/ui/card'
import BlogCard from '@/components/BlogCard.vue'
import { useRoute, useRouter } from 'vue-router'
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
    </div>

    <div v-if="isLoading" class="grid gap-6 sm:grid-cols-2">
      <Card v-for="i in posts.length" :key="i" class="animate-pulse h-[200px] bg-muted/50"></Card>
    </div>

    <div v-else-if="posts.length > 0">
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-2 mb-10">
        <router-link v-for="post in posts" :key="post.id" :to="{ name: 'post-detail', params: { id: post.id } }" class="block">
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