<script setup lang="ts">
import { ref } from 'vue'
import researchData from '../data/research.json'
import type { ResearchArea } from '../types'
import { getAssetUrl } from '../utils/assets'

const research = ref<ResearchArea[]>(researchData as ResearchArea[])
</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-4">Research Areas</h1>
      <p class="text-lg text-gray-600 text-center mb-12 max-w-4xl mx-auto">
        We focus on developing deep learning models essential for materials and processing, integrating experimental data from autonomous labs with simulation data based on computational materials science.
      </p>

      <div class="space-y-12">
        <section
          v-for="area in research"
          :key="area.id"
          :id="area.id"
          class="bg-white rounded-lg shadow-md overflow-hidden"
        >
          <div class="md:flex">
            <div class="md:w-2/5 relative overflow-hidden h-[280px] flex items-center justify-center">
              <img
                :src="getAssetUrl(area.image)"
                :alt="area.title"
                class="max-w-full max-h-full object-contain"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent"></div>
              <div class="absolute bottom-0 left-0 right-0 p-6">
                <h2 class="text-white font-bold text-2xl">{{ area.title }}</h2>
              </div>
            </div>
            <div class="md:w-3/5 p-8">
              <p class="text-gray-700 mb-6">{{ area.description }}</p>
              <h3 class="font-semibold text-gray-900 mb-3">Key Research Topics</h3>
              <ul class="space-y-2">
                <li
                  v-for="(detail, index) in area.details"
                  :key="index"
                  class="flex items-start"
                >
                  <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
