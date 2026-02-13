/**
 * Google Analytics 4 – loads gtag in-app when VITE_GA_MEASUREMENT_ID is set.
 */

const GA_ID = import.meta.env.VITE_GA_MEASUREMENT_ID as string | undefined

declare global {
  interface Window {
    dataLayer?: unknown[]
    gtag?: (...args: unknown[]) => void
  }
}

/** Same as Google’s gtag snippet: dataLayer + gtag stub, then 'js' + 'config', then load gtag.js. */
export function initGoogleAnalytics(): void {
  if (!GA_ID || typeof GA_ID !== 'string' || GA_ID.trim() === '') return

  window.dataLayer = window.dataLayer || []
  window.gtag = function gtag() {
    window.dataLayer!.push(arguments)
  }
  window.gtag('js', new Date())
  window.gtag('config', GA_ID)

  const script = document.createElement('script')
  script.async = true
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`
  document.head.appendChild(script)
}

export function trackPageView(path: string): void {
  if (!GA_ID || typeof window.gtag !== 'function') return
  window.gtag('config', GA_ID, { page_path: path })
}

export function trackEvent(eventName: string, params?: Record<string, unknown>): void {
  if (!GA_ID || typeof window.gtag !== 'function') return
  window.gtag('event', eventName, params)
}
