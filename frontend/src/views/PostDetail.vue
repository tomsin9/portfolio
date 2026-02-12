<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { apiBaseUrl } from '@/config/site'
import axios from 'axios'
import { marked } from 'marked'
import { useI18n } from 'vue-i18n'
import { formatDateTime } from '@/lib/formatDate'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'

import type { Post } from '@/types/blog'

const { t, locale } = useI18n()
const props = defineProps(['id'])
const post = ref<Post | null>(null)

onMounted(async () => {
  const response = await axios.get(`${apiBaseUrl}/api/v1/blog/${props.id}`)
  post.value = response.data
})
</script>

<template>
  <div v-if="post" class="container py-24 animate-in fade-in duration-700">
    <Breadcrumb class="mb-8">
      <BreadcrumbList>
        <BreadcrumbItem>
          <BreadcrumbLink as-child>
            <RouterLink to="/">{{ t('navbar.home') }}</RouterLink>
          </BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator />
        <BreadcrumbItem>
          <BreadcrumbLink as-child>
            <RouterLink to="/blog">{{ t('blog.title') }}</RouterLink>
          </BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator />
        <BreadcrumbItem>
          <BreadcrumbPage class="truncate max-w-[200px] sm:max-w-none">{{ post.title }}</BreadcrumbPage>
        </BreadcrumbItem>
      </BreadcrumbList>
    </Breadcrumb>

    <p class="text-sm text-muted-foreground mb-4">{{ formatDateTime(post.created_at, locale) }}</p>
    <h1 class="text-4xl font-bold tracking-tight mb-8">{{ post.title }}</h1>
    
    <article 
      class="prose dark:prose-invert prose-headings:font-semibold prose-pre:border max-w-none mt-12"
      v-html="marked(post.content ?? '')"
    ></article>
  </div>
</template>