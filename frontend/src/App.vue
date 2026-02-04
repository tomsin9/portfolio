<script setup lang="ts">
import { useDark } from '@vueuse/core'

import Hero from './components/landing/Hero.vue'
import BlogSection from './components/landing/BlogSection.vue'
import FloatingNavbar from './components/FloatingNavbar.vue'

const isDark = useDark({ initialValue: 'dark' })
</script>

<template>
  <div
    class="min-h-screen bg-background text-foreground antialiased transition-colors duration-300"
    :class="{ dark: isDark }"
  >
    
    <FloatingNavbar />

    <main>
      <Hero />
      <BlogSection />
      <!-- <section class="container py-12"></section> -->
    </main>

    <!-- <footer class="border-t border-border py-8">
      <div class="container text-center text-sm text-muted-foreground">
        © 2026 {{ siteConfig.author }}. Built with FastAPI, Vue 3, Tailwind CSS and shadcn/vue.
      </div>
    </footer> -->
  </div>
</template>

<style>
/* 確保字體符合 New York 風格的簡潔感 */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
</style>