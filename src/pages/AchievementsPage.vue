<script setup lang="ts">
import { ref, computed } from 'vue'
import journalsData from '../data/journals.json'
import conferencesData from '../data/conferences.json'
import preprintsData from '../data/preprints.json'
import IFData from '../data/IF.json'
import type { Publication } from '../types'

const journals = ref<Publication[]>((journalsData as Publication[]).sort((a, b) => {
  const idA = parseInt(a.id.replace('pub', ''))
  const idB = parseInt(b.id.replace('pub', ''))
  return idB - idA
}))
const conferences = ref<Publication[]>(conferencesData as Publication[])
const preprints = ref<Publication[]>(preprintsData as Publication[])
// ... (rest of script)

const activeTab = ref<'journals' | 'conferences' | 'preprints'>('journals')

const selectedYear = ref<number | null>(null)
const years = computed(() => {
  // Filter years based on active tab
  const activePubs = activeTab.value === 'journals' ? journals.value : 
                     activeTab.value === 'conferences' ? conferences.value : preprints.value
  const yearSet = new Set(activePubs.map(p => p.year))
  return Array.from(yearSet).sort((a, b) => b - a)
})

const filteredPublications = computed(() => {
  let filtered = activeTab.value === 'journals' ? journals.value : 
                 activeTab.value === 'conferences' ? conferences.value : preprints.value

  // Filter by year
  if (selectedYear.value) {
    filtered = filtered.filter(p => p.year === selectedYear.value)
  }
  
  return filtered
})
</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-12">Publications</h1>

      <!-- Tabs -->
      <!-- Tabs -->
      <div class="flex justify-center mb-8 gap-4">
        <button
          @click="activeTab = 'journals'"
          class="px-6 py-2 rounded-full font-medium text-sm transition-colors shadow-sm"
          :class="activeTab === 'journals' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'"
        >
          Journals
        </button>
        <button
          @click="activeTab = 'conferences'"
          class="px-6 py-2 rounded-full font-medium text-sm transition-colors shadow-sm"
          :class="activeTab === 'conferences' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'"
        >
          Conferences
        </button>
        <button
          @click="activeTab = 'preprints'"
          class="px-6 py-2 rounded-full font-medium text-sm transition-colors shadow-sm"
          :class="activeTab === 'preprints' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'"
        >
          Preprints
        </button>
      </div>



      <!-- Journals -->
      <div v-if="activeTab === 'journals'" class="space-y-6">
        <!-- Year Filter -->
        <div class="flex flex-wrap gap-2 justify-center mb-6">
          <button
            @click="selectedYear = null"
            class="px-4 py-1 rounded-full text-sm transition-colors"
            :class="selectedYear === null ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
          >
            All
          </button>
          <button
            v-for="year in years"
            :key="year"
            @click="selectedYear = year"
            class="px-4 py-1 rounded-full text-sm transition-colors"
            :class="selectedYear === year ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
          >
            {{ year }}
          </button>
        </div>

        <div class="space-y-4">
          <div
            v-for="pub in filteredPublications"
            :key="pub.id"
            class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
          >
            <div class="flex items-start gap-4">
              <span class="text-sm font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded">{{ pub.year }}</span>
              
              <!-- Highlight Image -->
              <div v-if="pub.highlightImage" class="flex-shrink-0 mr-2">
                <img :src="pub.highlightImage" :alt="pub.title" class="w-32 h-auto rounded-lg shadow-sm border border-gray-100 object-contain" />
              </div>

              <div class="flex-1">
                <h3 class="font-medium text-gray-900 mb-2">{{ pub.title }}</h3>
                <p class="text-sm text-gray-600 mb-2">
                  <span v-for="(author, index) in pub.authors" :key="index">
                    <span :class="{ 'font-bold': author.includes('^') }">{{ author.replace(/[*+^]/g, '') }}</span><sup v-if="author.includes('+')" class="text-blue-600">†</sup><sup v-if="author.includes('*')" class="text-blue-600">*</sup><span v-if="index < pub.authors.length - 1">, </span>
                  </span>
                </p>
                <p class="text-sm">
                  <span class="text-blue-600 font-medium">{{ pub.journal }}</span>
                  <span v-if="pub.volume" class="text-gray-500">, {{ pub.volume }}</span>
                  <span v-if="pub.pages" class="text-gray-500">, {{ pub.pages }}</span>
                  <span v-if="IFData[pub.journal as keyof typeof IFData]" class="text-blue-600 font-normal ml-1">({{ IFData[pub.journal as keyof typeof IFData] }})</span>
                </p>
                <a
                  v-if="pub.doi"
                  :href="`https://doi.org/${pub.doi}`"
                  target="_blank"
                  class="inline-flex items-center text-sm text-gray-500 hover:text-blue-600 mt-2"
                >
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  DOI: {{ pub.doi }}
                </a>
                

                <!-- Legend inside card -->
                <div v-if="pub.authors.some(a => a.includes('+'))" class="flex gap-4 mt-3 text-xs text-gray-500 border-t pt-2">
                  <div class="flex items-center">
                    <sup class="text-blue-600 mr-1">†</sup> Equally contributed
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Conferences -->
      <div v-if="activeTab === 'conferences'" class="space-y-6">
         <!-- Year Filter (Optional, reusing same logic for now or can be separate) -->
         <div class="flex flex-wrap gap-2 justify-center mb-6">
          <button
            @click="selectedYear = null"
            class="px-4 py-1 rounded-full text-sm transition-colors"
            :class="selectedYear === null ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
          >
            All
          </button>
          <button
            v-for="year in years"
            :key="year"
            @click="selectedYear = year"
            class="px-4 py-1 rounded-full text-sm transition-colors"
            :class="selectedYear === year ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
          >
            {{ year }}
          </button>
        </div>

        <div class="space-y-4">
          <div
            v-for="pub in filteredPublications"
            :key="pub.id"
            class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
          >
             <div class="flex items-start gap-4">
              <span class="text-sm font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded">{{ pub.year }}</span>
              <div class="flex-1">
                <h3 class="font-medium text-gray-900 mb-2">{{ pub.title }}</h3>
                <p class="text-sm text-gray-600 mb-2">
                  <span v-for="(author, index) in pub.authors" :key="index">
                    <span :class="{ 'font-bold': author.includes('^') }">{{ author.replace(/[*+^]/g, '') }}</span><sup v-if="author.includes('+')" class="text-blue-600">†</sup><sup v-if="author.includes('*')" class="text-blue-600">*</sup><span v-if="index < pub.authors.length - 1">, </span>
                  </span>
                </p>
                <div class="text-sm">
                  <div class="text-blue-600 font-medium mb-1">
                    {{ pub.journal }}
                    <span v-if="IFData[pub.journal as keyof typeof IFData]" class="text-blue-600 font-normal ml-1">({{ IFData[pub.journal as keyof typeof IFData] }})</span>
                  </div>
                  <a v-if="pub.link" :href="pub.link" target="_blank" class="text-gray-500 hover:text-blue-600 transition-colors inline-flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                    Link
                  </a>
                </div>

                <!-- Legend inside card -->
                <div v-if="pub.authors.some(a => a.includes('+'))" class="flex gap-4 mt-3 text-xs text-gray-500 border-t pt-2">
                  <div class="flex items-center">
                    <sup class="text-blue-600 mr-1">†</sup> Equally contributed
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Preprints -->
      <div v-if="activeTab === 'preprints'" class="space-y-6">
        <!-- Year Filter -->
        <div class="flex flex-wrap gap-2 justify-center mb-6">
          <button
            @click="selectedYear = null"
            class="px-4 py-1 rounded-full text-sm transition-colors"
            :class="selectedYear === null ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
          >
            All
          </button>
          <button
            v-for="year in years"
            :key="year"
            @click="selectedYear = year"
            class="px-4 py-1 rounded-full text-sm transition-colors"
            :class="selectedYear === year ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
          >
            {{ year }}
          </button>
        </div>

        <div class="space-y-4">
          <div
            v-for="pub in filteredPublications"
            :key="pub.id"
            class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
          >
            <div class="flex items-start gap-4">
              <span class="text-sm font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded">{{ pub.year }}</span>
              <div class="flex-1">
                <h3 class="font-medium text-gray-900 mb-2">{{ pub.title }}</h3>
                <p class="text-sm text-gray-600 mb-2">
                  <span v-for="(author, index) in pub.authors" :key="index">
                    <span :class="{ 'font-bold': author.includes('^') }">{{ author.replace(/[*+^]/g, '') }}</span><sup v-if="author.includes('+')" class="text-blue-600">†</sup><sup v-if="author.includes('*')" class="text-blue-600">*</sup><span v-if="index < pub.authors.length - 1">, </span>
                  </span>
                </p>
                <p class="text-sm">
                  <span class="text-blue-600 font-medium">{{ pub.journal }}</span>
                </p>
                <a
                  v-if="pub.doi"
                  :href="`https://doi.org/${pub.doi}`"
                  target="_blank"
                  class="inline-flex items-center text-sm text-gray-500 hover:text-blue-600 mt-2"
                >
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  DOI: {{ pub.doi }}
                </a>

                <!-- Legend inside card -->
                <div v-if="pub.authors.some(a => a.includes('+'))" class="flex gap-4 mt-3 text-xs text-gray-500 border-t pt-2">
                  <div class="flex items-center">
                    <sup class="text-blue-600 mr-1">†</sup> Equally contributed
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
