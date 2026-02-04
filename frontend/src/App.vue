<script setup lang="ts">
import Hero from './components/Hero.vue'
import { Button } from '@/components/ui/button'
import { Github, Laptop, Moon, Sun } from 'lucide-vue-next'

</script>

<template>
  <div class="min-h-screen bg-background text-foreground antialiased">
    
    <nav class="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div class="container flex h-16 items-center justify-between px-4 md:px-8">
        <div class="flex items-center gap-2">
          <Laptop class="h-6 w-6" />
          <span class="text-lg font-bold tracking-tight">TOM SIN</span>
        </div>
        
        <div class="flex items-center gap-4">
          <nav class="hidden md:flex items-center gap-6 text-sm font-medium">
            <a href="#" class="transition-colors hover:text-foreground/80 text-foreground">Projects</a>
            <a href="#" class="transition-colors hover:text-foreground/80 text-foreground/60">Blog</a>
            <a href="#" class="transition-colors hover:text-foreground/80 text-foreground/60">About</a>
          </nav>
          
          <div class="flex items-center gap-2">
            <Button variant="ghost" size="icon">
              <Github class="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon">
              <Sun class="h-5 w-5 dark:hidden" />
              <Moon class="hidden h-5 w-5 dark:block" />
            </Button>
          </div>
        </div>
      </div>
    </nav>

    <main>
      <Hero />
      
      <section class="container py-12">
        </section>
    </main>

    <footer class="border-t border-border py-8">
      <div class="container text-center text-sm text-muted-foreground">
        © 2026 Tom SIN. Built with FastAPI, Vue 3, Tailwind CSS and shadcn/vue.
      </div>
    </footer>
  </div>
</template>

<style>
/* 確保字體符合 New York 風格的簡潔感 */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
</style>