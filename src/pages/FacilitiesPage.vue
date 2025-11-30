<script setup lang="ts">
import { ref } from 'vue'
import facilitiesData from '../data/facilities.json'
import type { Facility } from '../types'
import { getAssetUrl } from '../utils/assets'

const facilities = ref<Facility[]>(facilitiesData as Facility[])
</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-4">Facilities</h1>
      <p class="text-lg text-gray-600 text-center mb-12 max-w-3xl mx-auto">
        Our laboratory is equipped with facilities for training the deep learing models and acquiring the materials data automatically.   
      </p>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div
          v-for="facility in facilities"
          :key="facility.id"
          class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
        >
          <div class="h-96 bg-gray-200 overflow-hidden relative flex items-center justify-center">
            <img
              v-if="facility.image"
              :src="getAssetUrl(facility.image)"
              :alt="facility.name"
              class="w-[90%] h-[90%] object-contain"
            />
            <div v-else class="w-full h-full bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center">
              <svg class="w-24 h-24 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
            </div>
          </div>
          <div class="p-6">
            <h2 class="text-xl font-bold text-gray-900 mb-4">{{ facility.name }}</h2>
            <p class="text-gray-600 mb-4">{{ facility.description }}</p>

            <div v-if="facility.manufacturer || facility.model" class="mb-4 text-sm bg-gray-50 p-3 rounded-md">
              <div v-if="facility.manufacturer" class="flex items-center gap-2 mb-1">
                <span class="font-semibold text-gray-700 w-24">Manufacturer:</span>
                <span class="text-gray-600">{{ facility.manufacturer }}</span>
              </div>
              <div v-if="facility.model" class="flex items-center gap-2">
                <span class="font-semibold text-gray-700 w-24">Model:</span>
                <span class="text-gray-600">{{ facility.model }}</span>
              </div>
            </div>

            <div v-if="facility.specifications && facility.specifications.length > 0">
              <h3 class="font-semibold text-gray-900 mb-2">Specifications</h3>
              <ul class="space-y-1">
                <li
                  v-for="(spec, index) in facility.specifications"
                  :key="index"
                  class="text-sm text-gray-600 flex items-start"
                >
                  <span class="text-blue-600 mr-2">•</span>
                  {{ spec }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
