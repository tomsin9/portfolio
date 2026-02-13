/**
 * Map vue-i18n locale to Intl locale for date formatting.
 * Use en-GB for British English; zh-HK for Traditional Chinese (Hong Kong).
 */
const localeMap: Record<string, string> = {
  en: 'en-GB',
  zh: 'zh-HK',
}

/** For datetime we use British English (en-GB) with AM/PM. */
const datetimeLocaleMap: Record<string, string> = {
  en: 'en-GB',
  zh: 'zh-HK',
}

export type DateFormatStyle = 'short' | 'medium' | 'long'

const defaultOptions: Intl.DateTimeFormatOptions = {
  year: 'numeric',
  month: 'short',
  day: 'numeric',
}

/**
 * Parse ISO date string. If no timezone (Z or ±HH:MM), treat as UTC so
 * backend UTC times display correctly in user's local timezone (e.g. Hong Kong).
 */
function parseAsUtcIfNeeded(isoDate: string): Date {
  const s = isoDate.trim()
  const hasOffset = /[Zz]$|[+-]\d{2}:?\d{2}$/.test(s)
  return new Date(hasOffset ? s : s + 'Z')
}

/**
 * Format an ISO date string for display, respecting i18n locale.
 * Use in components with: formatDate(isoDate, locale) where locale from useI18n().
 *
 * @param isoDate - ISO 8601 string (e.g. 2026-02-04T09:08:32.000078)
 * @param locale - Optional locale (e.g. 'en', 'zh'). When omitted, uses browser default.
 * @param style - Optional style; default is 'medium' (e.g. "Feb 4, 2026" / "2026年2月4日")
 * @returns Formatted date string, or original string if invalid
 */
export function formatDate(
  isoDate: string | undefined,
  locale?: string,
  style: DateFormatStyle = 'medium'
): string {
  if (isoDate == null || isoDate === '') return ''
  const d = parseAsUtcIfNeeded(isoDate)
  if (Number.isNaN(d.getTime())) return isoDate

  const intlLocale = locale ? localeMap[locale] ?? locale : undefined
  const options: Intl.DateTimeFormatOptions =
    style === 'short'
      ? { year: 'numeric', month: 'numeric', day: 'numeric' }
      : style === 'long'
        ? { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }
        : defaultOptions

  return new Intl.DateTimeFormat(intlLocale, options).format(d)
}

/**
 * Format an ISO date-time for display with time (AM/PM or 上午/下午).
 * Chinese uses 上午/下午; English uses British format (en-GB) with AM/PM.
 */
export function formatDateTime(isoDate: string | undefined, locale?: string): string {
  if (isoDate == null || isoDate === '') return ''
  const d = parseAsUtcIfNeeded(isoDate)
  if (Number.isNaN(d.getTime())) return isoDate

  const intlLocale = locale ? datetimeLocaleMap[locale] ?? localeMap[locale] ?? locale : undefined
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  }
  return new Intl.DateTimeFormat(intlLocale, options).format(d)
}
