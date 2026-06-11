<script setup lang="ts">
import { computed } from 'vue'
import type { Project } from '../../types'
import { localize } from '../../utils/i18n'

const props = defineProps<{
  project: Project
}>()

// Complete literal class strings (Tailwind scanner requirement)
const statusBorder: Record<Project['status'], string> = {
  ongoing: 'border-l-4 border-l-brand-500',
  completed: 'border-l-4 border-l-gray-300'
}

const roleBadgeClass = computed(() => {
  const roleEn = localize(props.project.role, 'en').toUpperCase()
  if (roleEn === 'PI') return 'bg-highlight-500 text-white'
  if (roleEn === 'CO-PI') return 'bg-gradient-to-r from-brand-600 to-accent-600 text-white'
  return 'bg-gray-500 text-white'
})
</script>

<template>
  <div class="glass-card card-lift overflow-hidden" :class="statusBorder[project.status]">
    <div class="p-6">
      <!-- Header with Title and Role Badge -->
      <div class="flex flex-wrap items-start justify-between gap-3 mb-4">
        <div class="flex-1">
          <h3 class="text-xl font-bold text-gray-900">{{ localize(project.title, 'en') }}</h3>
          <p class="text-lg text-gray-600">{{ localize(project.title, 'ko') }}</p>
        </div>
        <span
          class="px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap"
          :class="roleBadgeClass"
        >
          {{ localize(project.role, 'en') }}
        </span>
      </div>

      <!-- Project Details -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-100">
        <div>
          <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Period</p>
          <p class="text-gray-800 font-medium">{{ localize(project.period, 'en') }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Funding Agency</p>
          <p class="text-gray-800 font-medium">{{ localize(project.fundingAgency, 'en') }}</p>
        </div>
        <div v-if="project.fundingAmount">
          <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Budget</p>
          <p class="text-gray-800 font-medium">{{ localize(project.fundingAmount, 'en') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
