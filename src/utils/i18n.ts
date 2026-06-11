import type { BilingualText } from '../types'

/**
 * Resolve a possibly-bilingual field to a single language, preferring the
 * requested language and falling back to whichever translation exists.
 */
export function localize(
  field: string | Partial<BilingualText> | undefined | null,
  lang: 'en' | 'ko' = 'en'
): string {
  if (typeof field === 'string') return field
  if (field && typeof field === 'object') return field[lang] || field.en || field.ko || ''
  return ''
}
