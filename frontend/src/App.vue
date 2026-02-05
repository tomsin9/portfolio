<script setup lang="ts">
import { useDark } from '@vueuse/core'
import FloatingNavbar from './components/FloatingNavbar.vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const isDark = useDark({ initialValue: 'dark' })
</script>

<template>
  <div
    class="min-h-screen bg-background text-foreground antialiased transition-colors duration-300"
    :class="{ dark: isDark }"
  >
    <FloatingNavbar />

    <main>
      <router-view />
    </main>

    <!-- <footer class="border-t border-border py-8">
      <div class="container text-center text-sm text-muted-foreground">
        © 2026. Built with FastAPI, Vue 3, Tailwind CSS and shadcn/vue.
      </div>
    </footer> -->
  </div>
</template>