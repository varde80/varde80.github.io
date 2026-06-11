<script setup lang="ts">
import { ref } from 'vue'
import researchData from '../data/research.json'
import type { ResearchArea } from '../types'
import { getAssetUrl } from '../utils/assets'
import PageHero from '../components/common/PageHero.vue'

const research = ref<ResearchArea[]>(researchData as ResearchArea[])
</script>

<template>
  <div class="bg-gray-50 min-h-screen">
    <PageHero
      title="Research Areas"
      subtitle="We focus on developing deep learning models essential for materials and processing, integrating experimental data from autonomous labs with simulation data based on computational materials science."
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="space-y-12">
        <section
          v-for="area in research"
          :key="area.id"
          :id="area.id"
          class="glass-card card-lift overflow-hidden scroll-mt-24"
        >
          <div class="md:flex">
            <div class="md:w-2/5 relative overflow-hidden h-[280px] flex items-center justify-center bg-navy-900">
              <img
                :src="getAssetUrl(area.image)"
                :alt="area.title"
                class="max-w-full max-h-full object-contain"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-navy-950/85 via-navy-950/30 to-transparent"></div>
              <div class="absolute bottom-0 left-0 right-0 p-6">
                <h2 class="text-white font-bold text-2xl">{{ area.title }}</h2>
              </div>
            </div>
            <div class="md:w-3/5 p-8">
              <p class="text-gray-700 mb-6">{{ area.description }}</p>
              <h3 class="font-semibold gradient-text-strong mb-3">Key Research Topics</h3>
              <ul class="space-y-2">
                <li
                  v-for="(detail, index) in area.details"
                  :key="index"
                  class="flex items-start"
                >
                  <svg class="w-5 h-5 text-brand-600 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span class="text-gray-600">{{ detail }}</span>
                </li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
