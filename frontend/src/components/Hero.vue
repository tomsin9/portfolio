<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { siteConfig } from '@/config/site'

import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, Terminal, Mail } from 'lucide-vue-next'

const { locale, t } = useI18n()
// 根據當前語言 locale (zh/en) 自動計算要顯示嘅簡介
const personalInfo = computed(() => siteConfig.personal[locale.value])

function openInNewTab(url) {
  window.open(url, '_blank', 'noopener,noreferrer')
}
</script>

<template>
  <div class="relative w-full py-24 lg:py-32 overflow-hidden bg-background">
    <div class="absolute inset-0 z-0 bg-[radial-gradient(45%_45%_at_50%_50%,#f0f0f0_0,white_100%)] dark:bg-[radial-gradient(45%_45%_at_50%_50%,#18181b_0,#09090b_100%)]"></div>

    <div class="container relative z-10 mx-auto px-4 md:px-6">
      <div class="flex flex-col items-center space-y-4 text-center">
        
        <div class="inline-flex items-center rounded-full border border-zinc-200 bg-zinc-50 px-3 py-1 text-sm font-medium text-zinc-900 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-50 mb-4">
          <Terminal class="mr-2 h-4 w-4" />
          <span>v1.0.0 released</span>
        </div>

        <h1 class="text-4xl font-extrabold tracking-tighter lg:text-6xl" v-html="personalInfo.heroTitle"></h1>
        
        <p class="mx-auto max-w-[700px] text-zinc-500 md:text-xl dark:text-zinc-400">
            {{ personalInfo.about }}
        </p>

        <div class="flex flex-col gap-2 min-[400px]:flex-row pt-4">
          <Button size="lg" class="px-8 font-bold tracking-wide">
            View Projects
            <ArrowRight class="ml-2 h-4 w-4" />
          </Button>
          
          <Button variant="outline" size="lg" class="px-8" @click="openInNewTab(siteConfig.socials.email)">
            Contact Me
            <Mail class="ml-2 h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>