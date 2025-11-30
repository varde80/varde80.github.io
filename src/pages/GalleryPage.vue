<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import galleryData from '../data/gallery.json'
import type { GalleryImage } from '../types'

const images = ref<GalleryImage[]>(galleryData as GalleryImage[])

const selectedCategory = ref<string | null>(null)
const selectedImage = ref<GalleryImage | null>(null)
const currentImageIndices = ref<Record<string, number>>({})
let carouselInterval: number | null = null

const categories = computed(() => {
  const cats = new Set(images.value.map(img => img.category).filter(Boolean))
  return Array.from(cats)
})

const filteredImages = computed(() => {
  if (!selectedCategory.value) return images.value
  return images.value.filter(img => img.category === selectedCategory.value)
})

const openModal = (image: GalleryImage) => {
  selectedImage.value = image
}

const closeModal = () => {
  selectedImage.value = null
}

const getCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    group: 'Group Photo',
    conference: 'Conference',
    workshop: 'Workshop',
    graduation: 'Graduation',
    social: 'Social',
    seminar: 'Seminar'
  }
  return labels[category] || category
}

const startCarousel = () => {
  carouselInterval = window.setInterval(() => {
    images.value.forEach(image => {
      if (image.images && image.images.length > 1) {
        const currentIndex = currentImageIndices.value[image.id] || 0
        currentImageIndices.value[image.id] = (currentIndex + 1) % image.images.length
      }
    })
  }, 5000) // Change image every 3 seconds
}

onMounted(() => {
  // Initialize indices
  images.value.forEach(image => {
    currentImageIndices.value[image.id] = 0
  })
  startCarousel()
})

onUnmounted(() => {
  if (carouselInterval) {
    clearInterval(carouselInterval)
  }
})
</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-4">Gallery</h1>
      <p class="text-lg text-gray-600 text-center mb-12">Explore photos from our lab activities and events.</p>

      <!-- Category Filter -->
      <div class="flex flex-wrap gap-2 justify-center mb-8">
        <button
          @click="selectedCategory = null"
          class="px-4 py-2 rounded-full text-sm font-medium transition-colors"
          :class="selectedCategory === null ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
        >
          All
        </button>
        <button
          v-for="category in categories"
          :key="category"
          @click="selectedCategory = category ?? null"
          class="px-4 py-2 rounded-full text-sm font-medium transition-colors"
          :class="selectedCategory === category ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
        >
          {{ getCategoryLabel(category!) }}
        </button>
      </div>

      <!-- Image Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="image in filteredImages"
          :key="image.id"
          class="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer group"
          @click="openModal(image)"
        >
          <div class="aspect-video bg-gray-200 relative overflow-hidden">
            <img
              v-if="image.images && image.images.length > 0"
              :src="image.images[currentImageIndices[image.id] || 0]"
              :alt="image.title"
              class="w-full h-full object-cover transition-opacity duration-500"
            />
            <div v-else class="absolute inset-0 flex items-center justify-center text-gray-400">
              <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            
            <!-- Image Counter Indicator -->
            <div v-if="image.images && image.images.length > 1" class="absolute bottom-2 right-2 bg-black/50 text-white text-xs px-2 py-1 rounded-full">
              {{ (currentImageIndices[image.id] || 0) + 1 }} / {{ image.images.length }}
            </div>

            <div class="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors flex items-center justify-center">
              <svg class="w-10 h-10 text-white opacity-0 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
              </svg>
            </div>
          </div>
          <div class="p-4">
            <h3 class="font-medium text-gray-900">{{ image.title }}</h3>
            <p v-if="image.date" class="text-sm text-gray-500 mt-1">{{ image.date }}</p>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredImages.length === 0" class="text-center py-12">
        <p class="text-gray-500">No photos found in this category.</p>
      </div>
    </div>

    <!-- Image Modal -->
    <div
      v-if="selectedImage"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div class="aspect-video bg-gray-200 flex items-center justify-center relative">
          <img
            v-if="selectedImage.images && selectedImage.images.length > 0"
            :src="selectedImage.images[currentImageIndices[selectedImage.id] || 0]"
            :alt="selectedImage.title"
            class="w-full h-full object-contain"
          />
          <div v-else class="w-24 h-24 text-gray-400">
             <svg class="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
        <div class="p-6">
          <h3 class="text-xl font-bold text-gray-900">{{ selectedImage.title }}</h3>
          <p v-if="selectedImage.description" class="text-gray-600 mt-2">{{ selectedImage.description }}</p>
          <p v-if="selectedImage.date" class="text-sm text-gray-500 mt-2">{{ selectedImage.date }}</p>
        </div>
        <button
          @click="closeModal"
          class="absolute top-4 right-4 text-white hover:text-gray-300"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
