<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, provide } from 'vue'
import { useDark } from '@vueuse/core'
import FloatingNavbar from './components/FloatingNavbar.vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { Toaster } from '@/components/ui/sonner'
import 'vue-sonner/style.css'

import SeasonsFalling from 'vue-seasons-falling'

gsap.registerPlugin(ScrollTrigger)

const SEASONS_EFFECT_STORAGE_KEY = 'seasons-effect-on'

function getStoredSeasonsEffect(): boolean {
  try {
    const stored = localStorage.getItem(SEASONS_EFFECT_STORAGE_KEY)
    // Default off; only on if user has previously turned it on (stored 'true')
    return stored === 'true'
  } catch {
    return false
  }
}

const isDark = useDark({ initialValue: 'dark' })

const seasonsEffectOn = ref(getStoredSeasonsEffect())

function toggleSeason() {
  seasonsEffectOn.value = !seasonsEffectOn.value
}

watch(seasonsEffectOn, (on) => {
  try {
    localStorage.setItem(SEASONS_EFFECT_STORAGE_KEY, String(on))
  } catch {}
})

provide('toggleSeason', toggleSeason)
provide('seasonsEffectOn', seasonsEffectOn)

const mouseX = ref(50)
const mouseY = ref(50)

function onMouseMove(e: MouseEvent) {
  mouseX.value = (e.clientX / window.innerWidth) * 100
  mouseY.value = (e.clientY / window.innerHeight) * 100
}

onMounted(() => {
  window.addEventListener('mousemove', onMouseMove)
})
onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
})
</script>

<template>
  <div
    class="min-h-screen bg-background text-foreground antialiased transition-colors duration-300 relative overflow-hidden"
    :class="{ dark: isDark }"
  >
    <!-- Seasons falling effect (site-wide when on, can be toggled off) -->
    <SeasonsFalling
      v-if="seasonsEffectOn"
      :theme="isDark ? 'dark' : 'light'"
      :amount="200"
      autoSeason
      fullScreen
      mouseInteraction
    />

    <!-- Mouse-following glow (stronger in light mode so it's visible on white) -->
    <div
      class="pointer-events-none fixed inset-0 z-0"
      aria-hidden="true"
      :style="{
        background: `radial-gradient(
          circle 40vmax at ${mouseX}% ${mouseY}%,
          hsl(var(--primary) / ${isDark ? 0.04 : 0}),
          transparent 60%
        )`,
      }"
    />

    <div class="relative z-10">
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
    
    <Toaster position="top-center" />
  </div>
</template>