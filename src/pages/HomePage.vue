<script setup lang="ts">
import { computed, ref } from 'vue'
import researchData from '../data/research.json'
import galleryData from '../data/news.json'
import type { ResearchArea } from '../types'
import { getAssetUrl } from '../utils/assets'
import BaseCarousel from '../components/ui/BaseCarousel.vue'

const research = ref<ResearchArea[]>(researchData as ResearchArea[])

// Filter news from last 3 months and flatten into slides
const threeMonthsAgo = new Date()
threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3)

const gallerySlides = galleryData
  .filter(item => new Date(item.date) >= threeMonthsAgo)
  .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
  .flatMap(item =>
    item.images.map(image => ({
      image,
      title: item.title,
      description: item.description,
      date: item.date
    }))
  )

interface HeroSlide {
  image: string
  title: string
  subtitle: string
}

const heroSlides: HeroSlide[] = [
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

const currentGalleryIndex = ref(0)
const currentGalleryDescription = computed(
  () => gallerySlides[currentGalleryIndex.value]?.description ?? ''
)
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="relative min-h-[70vh] bg-navy-950 overflow-hidden">
      <BaseCarousel :slides="heroSlides" label="Lab highlights" class="min-h-[70vh]">
        <template #slide="{ slide }">
          <!-- Blurred cover backdrop fills the frame without cropping the foreground -->
          <img
            :src="getAssetUrl(slide.image)"
            alt=""
            aria-hidden="true"
            class="absolute inset-0 w-full h-full object-cover blur-2xl scale-110 opacity-40"
          />
          <img
            :src="getAssetUrl(slide.image)"
            :alt="slide.title"
            class="absolute inset-0 w-full h-full object-contain"
          />
          <div class="absolute inset-0 bg-gradient-to-r from-navy-950/90 via-navy-900/60 to-navy-950/70"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="text-center px-4">
              <h1 class="text-5xl md:text-7xl font-bold mb-4 gradient-text">{{ slide.title }}</h1>
              <p class="text-xl md:text-2xl text-slate-200 mb-8">{{ slide.subtitle }}</p>
              <RouterLink to="/contact" class="btn-gradient">
                Join Our Team
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </RouterLink>
            </div>
          </div>
        </template>
      </BaseCarousel>
    </section>

    <!-- About Section -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold gradient-text-strong mb-4">About Our Lab</h2>
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
        <h2 class="text-3xl font-bold gradient-text-strong text-center mb-12">Research Areas</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <RouterLink
            v-for="area in research"
            :key="area.id"
            :to="`/research#${area.id}`"
            class="glass-card card-lift overflow-hidden group focus-ring"
          >
            <div class="h-48 relative overflow-hidden flex items-center justify-center bg-navy-900">
              <img
                :src="getAssetUrl(area.image)"
                :alt="area.title"
                class="max-w-full max-h-full object-contain"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-navy-950/85 via-navy-950/30 to-transparent"></div>
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

    <!-- Gallery Section -->
    <section v-if="gallerySlides.length > 0" class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-bold gradient-text-strong">News</h2>
          <RouterLink
            to="/news"
            class="text-brand-600 hover:text-brand-700 font-medium flex items-center focus-ring rounded-md"
          >
            View All
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </RouterLink>
        </div>

        <!-- News Description -->
        <div class="mb-4 min-h-[3rem]">
          <p class="text-brand-700 font-semibold text-xl">{{ currentGalleryDescription }}</p>
        </div>

        <!-- Gallery Slideshow -->
        <div class="relative aspect-[3/1] max-h-[400px] bg-navy-950 rounded-2xl overflow-hidden">
          <BaseCarousel
            :slides="gallerySlides"
            :interval="30000"
            label="Recent news gallery"
            dots="right"
            @change="currentGalleryIndex = $event"
          >
            <template #slide="{ slide }">
              <img
                :src="getAssetUrl(slide.image)"
                :alt="slide.title"
                class="absolute inset-0 w-full h-full object-contain"
              />
            </template>
          </BaseCarousel>
        </div>
      </div>
    </section>
  </div>
</template>
