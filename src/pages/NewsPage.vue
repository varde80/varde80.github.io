<script setup lang="ts">
import { ref, computed } from 'vue'
import galleryData from '../data/news.json'
import type { GalleryImage } from '../types'
import PageHero from '../components/common/PageHero.vue'
import FilterPill from '../components/ui/FilterPill.vue'
import NewsCard from '../components/news/NewsCard.vue'
import NewsModal from '../components/news/NewsModal.vue'

const images = ref<GalleryImage[]>(galleryData as GalleryImage[])

const selectedCategory = ref<string | null>(null)
const selectedImage = ref<GalleryImage | null>(null)

const categories = computed(() => {
  const cats = new Set(images.value.map(img => img.category).filter(Boolean))
  return Array.from(cats)
})

const filteredImages = computed(() => {
  const sorted = [...images.value].sort((a, b) => new Date(b.date || 0).getTime() - new Date(a.date || 0).getTime())
  if (!selectedCategory.value) return sorted
  return sorted.filter(img => img.category === selectedCategory.value)
})

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
</script>

<template>
  <div class="bg-gray-50 min-h-screen">
    <PageHero title="News" subtitle="Explore photos from our lab activities and events.">
      <!-- Category Filter -->
      <div class="flex flex-wrap gap-2 mt-8">
        <FilterPill size="sm" :active="selectedCategory === null" @click="selectedCategory = null">
          All
        </FilterPill>
        <FilterPill
          v-for="category in categories"
          :key="category"
          size="sm"
          :active="selectedCategory === category"
          @click="selectedCategory = category ?? null"
        >
          {{ getCategoryLabel(category!) }}
        </FilterPill>
      </div>
    </PageHero>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Image Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <NewsCard
          v-for="image in filteredImages"
          :key="image.id"
          :item="image"
          @open="selectedImage = image"
        />
      </div>

      <!-- Empty State -->
      <div v-if="filteredImages.length === 0" class="text-center py-12">
        <p class="text-gray-500">No photos found in this category.</p>
      </div>
    </div>

    <!-- Image Modal -->
    <NewsModal v-if="selectedImage" :item="selectedImage" @close="selectedImage = null" />
  </div>
</template>
