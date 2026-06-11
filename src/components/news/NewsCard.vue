<script setup lang="ts">
import type { GalleryImage } from '../../types'
import { getAssetUrl } from '../../utils/assets'
import { useCarousel } from '../../composables/useCarousel'

const props = defineProps<{
  item: GalleryImage
}>()

const emit = defineEmits<{
  open: []
}>()

// Each card cycles its own images independently
const { current, pause, resume } = useCarousel({
  length: () => props.item.images?.length ?? 0,
  interval: 5000
})
</script>

<template>
  <button
    type="button"
    class="glass-card card-lift overflow-hidden group text-left w-full focus-ring"
    @click="emit('open')"
    @mouseenter="pause"
    @mouseleave="resume"
  >
    <div class="aspect-video bg-gray-200 relative overflow-hidden">
      <img
        v-if="item.images && item.images.length > 0"
        :src="getAssetUrl(item.images[current] || '')"
        :alt="item.title"
        class="w-full h-full object-cover transition-opacity duration-500"
      />
      <div v-else class="absolute inset-0 flex items-center justify-center text-gray-400">
        <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>

      <!-- Image Counter Indicator -->
      <div
        v-if="item.images && item.images.length > 1"
        class="absolute bottom-2 right-2 bg-black/50 text-white text-xs px-2 py-1 rounded-full"
      >
        {{ current + 1 }} / {{ item.images.length }}
      </div>

      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors flex items-center justify-center">
        <svg class="w-10 h-10 text-white opacity-0 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
        </svg>
      </div>
    </div>
    <div class="p-4">
      <h3 class="font-medium text-gray-900">{{ item.title }}</h3>
      <p v-if="item.date" class="text-sm text-gray-500 mt-1">{{ item.date }}</p>
    </div>
  </button>
</template>
