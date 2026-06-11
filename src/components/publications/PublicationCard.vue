<script setup lang="ts">
import { computed } from 'vue'
import type { Publication, RoleBadge } from '../../types'
import { getAssetUrl } from '../../utils/assets'
import AuthorList from './AuthorList.vue'
import BaseBadge from '../ui/BaseBadge.vue'

const props = withDefaults(
  defineProps<{
    pub: Publication
    kind?: 'journal' | 'conference'
    accent?: 'submission' | 'inpress' | 'published' | 'none'
    /** Lab member is first or corresponding author. */
    highlighted?: boolean
    impactFactor?: string
    roleBadge?: RoleBadge | null
  }>(),
  { kind: 'journal', accent: 'none', highlighted: false, impactFactor: undefined, roleBadge: null }
)

// Complete literal class strings (Tailwind scanner requirement)
const accentClasses: Record<string, string> = {
  submission: 'border-l-4 border-l-highlight-500',
  inpress: 'border-l-4 border-l-accent-500',
  published: 'border-l-4 border-l-transparent',
  none: 'border-l-4 border-l-transparent'
}

const borderClass = computed(() =>
  props.accent === 'published' && props.highlighted
    ? 'border-l-4 border-l-brand-500'
    : accentClasses[props.accent]
)

const hasEqualContribution = computed(() => props.pub.authors.some(a => a.includes('+')))
</script>

<template>
  <article class="glass-card card-lift p-6" :class="borderClass">
    <div class="flex gap-4">
      <!-- Highlight Image -->
      <div v-if="pub.highlightImage" class="flex-shrink-0 mr-2 hidden sm:block">
        <img
          :src="getAssetUrl(pub.highlightImage)"
          :alt="pub.title"
          class="max-w-[12rem] max-h-[8rem] rounded-lg shadow-sm border border-gray-100 object-contain"
        />
      </div>

      <div class="flex-1">
        <div class="flex items-start justify-between gap-2 mb-2">
          <h3 class="font-medium text-gray-900">
            {{ pub.title }}
            <span v-if="highlighted" class="sr-only">(lab member is first or corresponding author)</span>
          </h3>
          <BaseBadge v-if="roleBadge" :variant="roleBadge.variant" class="whitespace-nowrap">
            {{ roleBadge.text }}
          </BaseBadge>
        </div>

        <AuthorList :authors="pub.authors" class="mb-2" />

        <!-- Journal line -->
        <p v-if="kind === 'journal'" class="text-sm">
          <span class="text-brand-600 font-medium">{{ pub.journal }}</span>
          <span v-if="pub.volume" class="text-gray-500">, {{ pub.volume }}</span>
          <span v-if="pub.pages" class="text-gray-500">, {{ pub.pages }}</span>
          <span v-if="impactFactor" class="text-brand-600 font-normal ml-1">({{ impactFactor }})</span>
          <span v-if="accent === 'inpress' && pub.status === 'accepted'" class="text-brand-600 font-medium">, accepted</span>
        </p>

        <!-- Conference line -->
        <div v-else class="text-sm">
          <div class="text-brand-600 font-medium mb-1 flex items-center flex-wrap gap-2">
            <span>{{ pub['Conference Name'] || pub.journal }}</span>
            <BaseBadge
              v-if="pub.scope"
              :variant="pub.scope === 'international' ? 'soft-indigo' : 'soft-emerald'"
              class="whitespace-nowrap"
            >
              {{ pub.scope === 'international' ? 'International' : 'Domestic' }}
            </BaseBadge>
          </div>
          <div v-if="pub.Venue" class="text-gray-500 text-xs mb-1">
            {{ pub.Venue }}
            <span v-if="pub['start date']"> · {{ pub['start date'] }} - {{ pub['end date'] }}</span>
          </div>
          <a
            v-if="pub.link"
            :href="pub.link"
            target="_blank"
            rel="noopener noreferrer"
            class="text-gray-500 hover:text-brand-600 transition-colors inline-flex items-center focus-ring rounded"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            Link
          </a>
        </div>

        <!-- DOI link (journals) -->
        <a
          v-if="kind === 'journal' && pub.doi"
          :href="`https://doi.org/${pub.doi}`"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center text-sm text-gray-500 hover:text-brand-600 mt-2 focus-ring rounded"
        >
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          DOI: {{ pub.doi }}
        </a>

        <!-- Equal-contribution legend -->
        <div v-if="hasEqualContribution" class="flex gap-4 mt-3 text-xs text-gray-500 border-t border-gray-200 pt-2">
          <div class="flex items-center">
            <sup class="text-brand-600 mr-1">†</sup> Equally contributed
          </div>
        </div>
      </div>
    </div>
  </article>
</template>
