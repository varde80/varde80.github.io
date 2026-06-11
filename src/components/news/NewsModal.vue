<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import type { GalleryImage } from '../../types'
import { getAssetUrl } from '../../utils/assets'
import { useCarousel } from '../../composables/useCarousel'

const props = defineProps<{
  item: GalleryImage
}>()

const emit = defineEmits<{
  close: []
}>()

const closeButton = ref<HTMLButtonElement | null>(null)

// Manual-only navigation inside the modal
const { current, next, prev } = useCarousel({
  length: () => props.item.images?.length ?? 0,
  autoplay: false
})

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    emit('close')
  } else if (e.key === 'ArrowLeft') {
    prev()
  } else if (e.key === 'ArrowRight') {
    next()
  }
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  closeButton.value?.focus()
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4"
    role="dialog"
    aria-modal="true"
    :aria-label="item.title"
    @click.self="emit('close')"
  >
    <div class="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden relative">
      <div class="aspect-video bg-gray-200 flex items-center justify-center relative">
        <img
          v-if="item.images && item.images.length > 0"
          :src="getAssetUrl(item.images[current] || '')"
          :alt="item.title"
          class="w-full h-full object-contain"
        />
        <div v-else class="w-24 h-24 text-gray-400">
          <svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>

        <!-- Prev/Next inside modal for multi-image items -->
        <template v-if="item.images && item.images.length > 1">
          <button
            @click="prev"
            aria-label="Previous image"
            class="absolute left-3 top-1/2 -translate-y-1/2 bg-black/40 hover:bg-black/60 text-white p-2 rounded-full focus-ring"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button
            @click="next"
            aria-label="Next image"
            class="absolute right-3 top-1/2 -translate-y-1/2 bg-black/40 hover:bg-black/60 text-white p-2 rounded-full focus-ring"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
          <div class="absolute bottom-2 right-2 bg-black/50 text-white text-xs px-2 py-1 rounded-full">
            {{ current + 1 }} / {{ item.images.length }}
          </div>
        </template>
      </div>
      <div class="p-6">
        <h3 class="text-xl font-bold text-gray-900">{{ item.title }}</h3>
        <p v-if="item.description" class="text-gray-600 mt-2">{{ item.description }}</p>
        <p v-if="item.date" class="text-sm text-gray-500 mt-2">{{ item.date }}</p>
      </div>
      <button
        ref="closeButton"
        @click="emit('close')"
        aria-label="Close"
        class="absolute top-4 right-4 bg-black/40 hover:bg-black/60 text-white p-1.5 rounded-full focus-ring"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>
