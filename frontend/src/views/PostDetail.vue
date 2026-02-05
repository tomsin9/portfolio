<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'

const props = defineProps(['id'])
const post = ref<any>(null)

onMounted(async () => {
  const response = await axios.get(`http://localhost:8000/api/v1/blog/${props.id}`)
  post.value = response.data
})
</script>

<template>
  <div v-if="post" class="container max-w-4xl py-24 animate-in fade-in duration-700">
    <router-link to="/" class="text-sm text-muted-foreground hover:text-primary mb-8 inline-block">
      ← Back to home
    </router-link>
    
    <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-4">{{ post.title }}</h1>
    <p class="text-muted-foreground mb-8">{{ new Date(post.date).toLocaleDateString() }}</p>
    
    <article 
      class="prose dark:prose-invert max-w-none mt-12"
      v-html="marked(post.content)"
    ></article>
  </div>
</template>