<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { apiBaseUrl } from '@/config/site'
import axios from 'axios'
import { marked } from 'marked'
import { useI18n } from 'vue-i18n'
import { formatDateTime } from '@/lib/formatDate'
import { ArrowLeftIcon } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
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
  <div v-if="post" class="container pt-12 pb-32 lg:pt-20 lg:pb-40 animate-in fade-in duration-700">
    
    <Button as="a" href="/" variant="link" class="p-0 h-auto mb-4 text-muted-foreground hover:text-foreground">
      <ArrowLeftIcon class="w-4 h-4" />
      {{ t('system.backToHome') }}
    </Button>

    <div class="flex items-center gap-2 mb-4">
      <div v-for="tag in post.tags" :key="tag">
        <span class="text-[10px] uppercase tracking-widest font-bold px-2 py-0.5 bg-secondary text-secondary-foreground rounded">
          {{ tag }}
        </span>
      </div>
    </div>
    <h1 class="text-4xl font-bold tracking-tight mb-4">{{ post.title }}</h1>
    <p class="text-sm text-muted-foreground mb-8">{{ formatDateTime(post.created_at, locale) }}</p>

    <article 
      class="prose dark:prose-invert prose-headings:font-semibold prose-pre:border max-w-none mt-12"
      v-html="marked(post.content ?? '')"
    ></article>
  </div>
</template>