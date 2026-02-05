<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { siteConfig } from '@/config/site'

import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, Mail, Code, Github, Linkedin, Instagram } from 'lucide-vue-next'

const { locale, t } = useI18n()
// 根據當前語言 locale (zh/en) 自動計算要顯示嘅簡介
const personalInfo = computed(() => siteConfig.personal[locale.value])

function openInNewTab(url) {
  window.open(url, '_blank', 'noopener,noreferrer')
}

function scrollToContact() {
  const el = document.getElementById('contact')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

</script>

<template>
  <div class="relative w-full py-24 lg:py-32 overflow-hidden bg-background">
    <div class="absolute inset-0 z-0 bg-[radial-gradient(45%_45%_at_50%_50%,#f0f0f0_0,white_100%)] dark:bg-[radial-gradient(45%_45%_at_50%_50%,#18181b_0,#09090b_100%)]"></div>

    <div class="container relative z-10 mx-auto px-4 md:px-6">
      <div class="flex flex-col items-center space-y-4 text-center">
        
        <div class="inline-flex items-center rounded-full border border-secondary bg-secondary px-3 py-1 text-sm font-medium text-secondary-foreground mb-4">
          <Code class="mr-2 h-4 w-4" />
          <span>Full Stack Web Developer</span>
        </div>

        <h1 class="text-4xl font-extrabold tracking-tighter lg:text-6xl" v-html="personalInfo.heroTitle"></h1>
        
        <p class="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
            {{ personalInfo.about }}
        </p>

        <div class="flex flex-col gap-2 min-[400px]:flex-row justify-center items-center pt-4">
          <Button size="lg" class="px-7 font-bold tracking-wide">
            {{ t('system.viewProjects') }}
            <ArrowRight class="ml-2 h-4 w-4" />
          </Button>

          <Button size="lg" variant="outline" class="px-7 font-bold tracking-wide" as="a" href="#contact" @click.prevent="scrollToContact">
            {{ t('system.contactMe') }}
          </Button>

          <!-- <div class="flex flex-row gap-2">
            <Button
              variant="outline"
              size="icon-lg"
              aria-label="LinkedIn"
              class="social-link"
              data-social="linkedin"
              @click="openInNewTab(siteConfig.socials.linkedin)"
            >
              <Linkedin class="h-4 w-4" />
              <span class="sr-only">{{ t('system.linkedin') }}</span>
            </Button>

            <Button
              variant="outline"
              size="icon-lg"
              aria-label="GitHub"
              class="social-link"
              data-social="github"
              @click="openInNewTab(siteConfig.socials.github)"
            >
              <Github class="h-4 w-4" />
              <span class="sr-only">{{ t('system.github') }}</span>
            </Button>

            <Button
              variant="outline"
              size="icon-lg"
              aria-label="Instagram"
              class="social-link"
              data-social="instagram"
              @click="openInNewTab(siteConfig.socials.instagram)"
            >
              <Instagram class="h-4 w-4" />
              <span class="sr-only">{{ t('system.instagram') }}</span>
            </Button>

            <Button
              variant="outline"
              size="icon-lg"
              aria-label="Email"
              class="social-link"
              data-social="email"
              @click="openInNewTab(siteConfig.socials.email)"
            >
              <Mail class="h-4 w-4" />
              <span class="sr-only">{{ t('system.contactMe') }}</span>
            </Button>
          </div> -->
        </div>
      </div>
    </div>
  </div>
</template>