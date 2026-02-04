// src/config/site.ts

/** API base URL (no trailing slash). Use VITE_API_BASE_URL in .env for environment-specific value. */
const env = (import.meta as unknown as { env?: { VITE_API_BASE_URL?: string } }).env
export const apiBaseUrl = env?.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export const siteConfig = {
    siteUrl: "https://tomsinp.com",
    siteTitle: "Tom Sin - Full-Stack Web Developer",
    author: "Tom SIN",
    keywords: "Tom Sin, Full-Stack Web Developer, Django, Vue.js, Python, web development, portfolio",
    description: "Tom Sin is a full-stack web developer specializing in modern web technologies. Explore my portfolio, blog, and projects.",
    ogImage: "/sin/og-image-square.png",
    socials: {
        github: "https://github.com/tomsin9/",
        linkedin: "https://linkedin.com/in/tom-sin/",
        instagram: "https://instagram.com/sin9_",
        email: "mailto:contact@tomsinp.com"
    },
    personal: {
        zh: {
            heroTitle: "Tom <span class='text-zinc-500'>SIN</span>",
            about: "一位來自香港的開發者，擅長於從零開始構建簡潔且實用的網站及網頁應用程式。",
            location: "香港"
        },
        en: {
            heroTitle: "Tom <span class='text-zinc-500'>SIN</span>",
            about: "A developer based in Hong Kong. I specialize in building clean, functional websites and web applications from scratch.",
            location: "Hong Kong"
        }
    }
}