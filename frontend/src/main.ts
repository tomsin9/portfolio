import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import './style.css'

import zh from './locales/zh.json'
import en from './locales/en.json'

const i18n = createI18n({
    legacy: false, // 必須要 set 做 false 先可以用 Composition API (useI18n)
    locale: 'en',  // 預設語言
    fallbackLocale: 'en',
    messages: {
        en: en,
        zh: zh
    },
})

const app = createApp(App)

app.use(router)
app.use(i18n)

app.mount('#app')