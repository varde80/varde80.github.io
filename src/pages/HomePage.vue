<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import researchData from '../data/research.json'
import journalsData from '../data/journals.json'
import conferencesData from '../data/conferences.json'
import preprintsData from '../data/preprints.json'
import galleryData from '../data/news.json'
import type { ResearchArea, Publication } from '../types'
import { getAssetUrl } from '../utils/assets'

const research = ref<ResearchArea[]>(researchData as ResearchArea[])

// Flatten gallery images into slides
const gallerySlides = galleryData.flatMap(item =>
  item.images.map(image => ({
    image,
    title: item.title,
    description: item.description,
    date: item.date
  }))
)
const recentPublications = ref<Publication[]>(
  ([...journalsData, ...conferencesData, ...preprintsData] as Publication[])
    .sort((a, b) => {
      // Sort by year descending, then by id descending
      if (b.year !== a.year) return b.year - a.year
      const idA = parseInt(a.id.replace('pub', ''))
      const idB = parseInt(b.id.replace('pub', ''))
      return idB - idA
    })
    .slice(0, 5)
)

const heroSlides = [
  {
    image: '/images/hero/slide1.png',
    title: 'AI for Materials Lab',
    subtitle: 'Exploring the secrets of materials using AI'
  },
  {
    image: '/images/hero/slide2.png',
    title: 'Cutting-edge Research',
    subtitle: 'Investigating future materials with advanced Deep Learning techniques'
  },
  {
    image: '/images/hero/slide3.png',
    title: 'Join Our Team',
    subtitle: 'We are looking for passionate researchers to join us'
  }
]

const currentSlide = ref(0)

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % heroSlides.length
}

const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + heroSlides.length) % heroSlides.length
}

const heroInterval = setInterval(nextSlide, 5000)

// Gallery slideshow
const currentGallerySlide = ref(0)

const nextGallerySlide = () => {
  if (gallerySlides.length > 0) {
    currentGallerySlide.value = (currentGallerySlide.value + 1) % gallerySlides.length
  }
}

const prevGallerySlide = () => {
  if (gallerySlides.length > 0) {
    currentGallerySlide.value = (currentGallerySlide.value - 1 + gallerySlides.length) % gallerySlides.length
  }
}

const galleryInterval = setInterval(nextGallerySlide, 4000)

onUnmounted(() => {
  clearInterval(heroInterval)
  clearInterval(galleryInterval)
})
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="relative aspect-[5/2] bg-gray-900 overflow-hidden">
      <div
        v-for="(slide, index) in heroSlides"
        :key="index"
        class="absolute inset-0 transition-opacity duration-1000"
        :class="currentSlide === index ? 'opacity-100' : 'opacity-0'"
      >
        <img :src="getAssetUrl(slide.image)" :alt="slide.title" class="absolute inset-0 w-full h-full object-contain" />
        <div class="absolute inset-0 bg-gradient-to-r from-blue-900/80 to-gray-900/60"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="text-center text-white px-4">
            <h1 class="text-5xl md:text-7xl font-bold mb-4" style="color: #F0980C">{{ slide.title }}</h1>
            <p class="text-xl md:text-2xl text-gray-200">{{ slide.subtitle }}</p>
          </div>
        </div>
      </div>

      <!-- Slide Controls -->
      <button
        @click="prevSlide"
        class="absolute left-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/40 text-white p-2 rounded-full transition-colors"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <button
        @click="nextSlide"
        class="absolute right-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/40 text-white p-2 rounded-full transition-colors"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <!-- Slide Indicators -->
      <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex space-x-2">
        <button
          v-for="(_, index) in heroSlides"
          :key="index"
          @click="currentSlide = index"
          class="w-3 h-3 rounded-full transition-colors"
          :class="currentSlide === index ? 'bg-white' : 'bg-white/50'"
        ></button>
      </div>
    </section>

    <!-- About Section -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">About Our Lab</h2>
          <p class="text-lg text-gray-600 max-w-7xl mx-auto">
            Our lab conducts research on AI for materials and processing.
            We work on property prediction, automation and acceleration of materials analysis, materials design, and process optimization by leveraging data generated from autonomous laboratories and computational science.
            By integrating these data sources with advanced AI models, we aim to develop innovative and efficient solutions for next-generation materials research.
          </p>
        </div>
      </div>
    </section>

    <!-- Research Areas -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Research Areas</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <RouterLink
            v-for="area in research"
            :key="area.id"
            :to="`/research#${area.id}`"
            class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow group"
          >
            <div class="h-48 relative overflow-hidden flex items-center justify-center">
              <img
                :src="getAssetUrl(area.image)"
                :alt="area.title"
                class="max-w-full max-h-full object-contain"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent"></div>
              <div class="absolute bottom-0 left-0 right-0 p-4">
                <h3 class="text-white font-semibold text-lg leading-tight">
                  {{ area.title }}
                </h3>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Recent Publications -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900">Recent Publications</h2>
          <RouterLink
            to="/achievements"
            class="text-blue-600 hover:text-blue-800 font-medium flex items-center"
          >
            View All
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </RouterLink>
        </div>
        <div class="space-y-4">
          <div
            v-for="pub in recentPublications"
            :key="pub.id"
            class="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors"
          >
            <h3 class="font-medium text-gray-900 mb-2">{{ pub.title }}</h3>
            <p class="text-sm text-gray-600 mb-1">
                <span v-for="(author, index) in pub.authors" :key="index">
                  <span :class="{ 'font-bold': author.includes('^') }">{{ author.replace(/[*+^]/g, '') }}</span><sup v-if="author.includes('*')" class="text-blue-600">*</sup><span v-if="index < pub.authors.length - 1">, </span>
                </span>
              </p>
            <p class="text-sm text-blue-600">
              {{ pub.journal }} ({{ pub.year }})
              <span v-if="pub.volume">, {{ pub.volume }}</span>
              <span v-if="pub.pages">, {{ pub.pages }}</span>
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Gallery Section -->
    <section v-if="gallerySlides.length > 0" class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900">News</h2>
          <RouterLink
            to="/gallery"
            class="text-blue-600 hover:text-blue-800 font-medium flex items-center"
          >
            View All
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </RouterLink>
        </div>

        <!-- Gallery Slideshow -->
        <div class="relative aspect-[3/1] max-h-[400px] bg-gray-900 rounded-lg overflow-hidden">
          <div
            v-for="(slide, index) in gallerySlides"
            :key="index"
            class="absolute inset-0 transition-opacity duration-1000"
            :class="currentGallerySlide === index ? 'opacity-100' : 'opacity-0'"
          >
            <img :src="getAssetUrl(slide.image)" :alt="slide.title" class="absolute inset-0 w-full h-full object-contain" />
            <div class="absolute inset-0 bg-gradient-to-b from-black/60 via-transparent to-transparent"></div>
            <div class="absolute top-0 left-0 right-0 p-6">
              <p class="text-white font-bold text-2xl drop-shadow-lg">{{ slide.description }}</p>
            </div>
          </div>

          <!-- Slide Controls -->
          <button
            @click="prevGallerySlide"
            class="absolute left-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/40 text-white p-2 rounded-full transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button
            @click="nextGallerySlide"
            class="absolute right-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/40 text-white p-2 rounded-full transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <!-- Slide Indicators -->
          <div class="absolute bottom-4 right-4 flex space-x-2">
            <button
              v-for="(_, index) in gallerySlides"
              :key="index"
              @click="currentGallerySlide = index"
              class="w-2 h-2 rounded-full transition-colors"
              :class="currentGallerySlide === index ? 'bg-white' : 'bg-white/50'"
            ></button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
