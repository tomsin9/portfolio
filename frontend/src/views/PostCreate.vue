<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { apiBaseUrl } from '@/config/site'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { auth } from '@/store/auth'
import { ArrowLeftIcon, SaveIcon, XIcon, PlusIcon } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { toast } from 'vue-sonner'
import Editor from '@/components/Editor.vue'

const { t } = useI18n()
const router = useRouter()

const isSaving = ref(false)
const newTag = ref('')

const form = reactive({
  title: '',
  excerpt: '',
  content: '',
  tags: [] as string[],
  is_published: false
})

onMounted(() => {
  if (!auth.isAdmin) router.replace('/blog')
})

const addTag = () => {
  const tag = newTag.value.trim()
  if (!tag) return
  if (form.tags.includes(tag)) {
    newTag.value = ''
    return
  }
  form.tags.push(tag)
  newTag.value = ''
}

const removeTag = (index: number) => {
  form.tags.splice(index, 1)
}

const saveCreate = async () => {
  const titleTrimmed = form.title.trim()
  const contentTrimmed = form.content.trim()
  if (!titleTrimmed) {
    toast.error(t('blog.titleRequired'))
    return
  }
  if (!contentTrimmed) {
    toast.error(t('blog.contentRequired'))
    return
  }

  isSaving.value = true
  try {
    await axios.post(
      `${apiBaseUrl}/api/v1/blog/`,
      {
        title: titleTrimmed,
        excerpt: form.excerpt.trim() || undefined,
        content: contentTrimmed,
        tags: form.tags,
        is_published: form.is_published
      },
      { headers: { Authorization: `Bearer ${auth.token}` } }
    )
    toast.success(t('blog.createPostSuccess'))
    await router.push('/blog')
  } catch (err: unknown) {
    console.error(err)
    const msg =
      axios.isAxiosError(err) && err.response?.data?.detail
        ? String(err.response.data.detail)
        : axios.isAxiosError(err) && err.response?.status === 401
          ? t('auth.pleaseLogInAgain')
          : 'Failed to create post'
    toast.error(msg)
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <div v-if="auth.isAdmin" class="container pt-12 pb-32 lg:pt-20 lg:pb-40 animate-in fade-in duration-700">
    <div class="flex justify-between items-center mb-4">
      <Button as="a" href="/blog" variant="link" class="p-0 h-auto mb-4 text-muted-foreground hover:text-foreground">
        <ArrowLeftIcon class="w-4 h-4" />
        {{ t('navbar.blog') }}
      </Button>
      <div class="flex gap-2 mb-4">
        <Button @click="saveCreate" :disabled="isSaving" variant="default" size="sm">
          <SaveIcon class="w-4 h-4 mr-2" />
          {{ isSaving ? t('system.saving') : t('blog.createPost') }}
        </Button>
        <Button as="a" href="/blog" variant="ghost" size="sm">
          <XIcon class="w-4 h-4 mr-2" />
          {{ t('system.cancel') }}
        </Button>
      </div>
    </div>

    <!-- Tags -->
    <div class="flex flex-wrap items-center gap-2 mb-4">
      <span
        v-for="(tag, index) in form.tags"
        :key="`${tag}-${index}`"
        class="inline-flex items-center gap-1 text-[10px] uppercase tracking-widest font-bold pl-2 pr-1 py-0.5 bg-secondary text-secondary-foreground rounded"
      >
        {{ tag }}
        <button
          type="button"
          aria-label="Remove tag"
          class="rounded hover:bg-secondary-foreground/20 p-0.5"
          @click="removeTag(index)"
        >
          <XIcon class="w-3 h-3" />
        </button>
      </span>
      <div class="inline-flex items-center gap-1">
        <input
          v-model="newTag"
          type="text"
          class="h-6 w-24 rounded border border-input bg-background px-2 text-[10px] uppercase tracking-widest focus:outline-none focus:ring-1 focus:ring-ring"
          :placeholder="t('blog.addTag')"
          @keydown.enter.prevent="addTag"
        />
        <Button type="button" variant="ghost" size="sm" class="h-6 w-6 p-0" @click="addTag">
          <PlusIcon class="w-3 h-3" />
        </Button>
      </div>
      <label class="inline-flex items-center gap-2 ml-2 text-sm text-muted-foreground">
        <input
          v-model="form.is_published"
          type="checkbox"
          class="rounded border-input text-primary focus:ring-ring"
        />
        {{ t('blog.published') }}
      </label>
    </div>

    <!-- Title (required) -->
    <div class="mb-4">
      <input
        v-model="form.title"
        class="text-2xl md:text-4xl font-bold tracking-tight w-full bg-transparent border-b border-primary focus:outline-none py-1"
        :placeholder="t('blog.titlePlaceholder')"
      />
    </div>

    <!-- Excerpt -->
    <div class="mb-4">
      <label class="block text-sm font-medium text-muted-foreground mb-1">{{ t('blog.excerpt') }}</label>
      <textarea
        v-model="form.excerpt"
        rows="2"
        class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        :placeholder="t('blog.excerptPlaceholder')"
      />
    </div>

    <!-- Content (required) -->
    <div class="mt-12">
      <label class="block text-sm font-medium text-muted-foreground mb-1">{{ t('blog.content') }} *</label>
      <div class="animate-in zoom-in-95 duration-200">
        <Editor v-model="form.content" />
      </div>
    </div>
  </div>
</template>
