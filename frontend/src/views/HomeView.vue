<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Hero from '../components/landing/Hero.vue'
import BlogSection from '../components/landing/BlogSection.vue'
import ContactSection from '../components/landing/ContactSection.vue'

const route = useRoute()

onMounted(() => {
  if (route.hash) {
    const target = route.hash.slice(1)
    setTimeout(() => {
      const el = document.getElementById(target)
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    }, 300)
  }
})
</script>

<template>
  <Hero />
  <BlogSection />
  <ContactSection />
</template>