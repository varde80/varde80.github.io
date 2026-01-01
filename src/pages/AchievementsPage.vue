<script setup lang="ts">
import { ref, computed } from 'vue'
import journalsData from '../data/journals.json'
import conferencesData from '../data/conferences.json'
import membersData from '../data/members.json'
import professorData from '../data/professor.json'
import IFData from '../data/IF.json'
import type { Publication, MembersData, Professor } from '../types'
import { getAssetUrl } from '../utils/assets'

const journals = ref<Publication[]>(journalsData as Publication[])
const conferences = ref<Publication[]>(conferencesData as Publication[])
const members = membersData as MembersData
const professor = professorData as Professor

// Build list of all member names for filtering
const allMemberNames = computed(() => {
  const names: string[] = [professor.name]
  members.researchers.forEach(m => names.push(m.name))
  members.phdStudents.forEach(m => names.push(m.name))
  members.msStudents.forEach(m => names.push(m.name))
  return names
})

// Selected member filter (null = show all)
const selectedMember = ref<string | null>(null)

// Check if a publication has a specific member as author
const hasMember = (pub: Publication, memberName: string): boolean => {
  return pub.authors.some(a => {
    if (!a) return false
    const cleanName = a.replace(/[*+^]/g, '').trim().toLowerCase()
    // Check if the member name matches (partial match for flexibility)
    const nameParts = memberName.toLowerCase().split(' ')
    return nameParts.every(part => cleanName.includes(part))
  })
}

// Determine the role of a member in a publication
const getAuthorRole = (pub: Publication, memberName: string): 'corresponding' | 'first' | 'co-author' | null => {
  const authors = pub.authors
  const nameParts = memberName.toLowerCase().split(' ')

  for (let i = 0; i < authors.length; i++) {
    const author = authors[i]
    if (!author) continue
    const cleanName = author.replace(/[*+^]/g, '').trim().toLowerCase()

    if (nameParts.every(part => cleanName.includes(part))) {
      if (author.includes('*')) {
        return 'corresponding'
      }
      if (i === 0) {
        return 'first'
      }
      return 'co-author'
    }
  }
  return null
}

const getRoleBadge = (role: string | null) => {
  switch (role) {
    case 'corresponding':
      return { text: 'Corresponding', class: 'bg-purple-100 text-purple-700' }
    case 'first':
      return { text: 'First Author', class: 'bg-green-100 text-green-700' }
    case 'co-author':
      return { text: 'Co-Author', class: 'bg-gray-100 text-gray-600' }
    default:
      return null
  }
}

const activeTab = ref<'journals' | 'conferences'>('journals')

// Filter journals by selected member
const filteredJournals = computed(() => {
  if (selectedMember.value) {
    return journals.value.filter(p => hasMember(p, selectedMember.value!))
  }
  return journals.value
})

// Filter conferences by selected member
const filteredConferences = computed(() => {
  if (selectedMember.value) {
    return conferences.value.filter(p => hasMember(p, selectedMember.value!))
  }
  return conferences.value
})

// Separate preprint/submitted from published journals
const inSubmission = computed(() => {
  return filteredJournals.value
    .filter(p => (p as any).status)
    .sort((a, b) => {
      const idA = parseInt(a.id.replace(/[^0-9]/g, ''))
      const idB = parseInt(b.id.replace(/[^0-9]/g, ''))
      return idB - idA
    })
})

// Published journals grouped by year (newest first)
const publishedByYear = computed(() => {
  const published = filteredJournals.value.filter(p => !(p as any).status)
  const years = [...new Set(published.map(p => p.year))].sort((a, b) => b - a)
  return years.map(year => ({
    year,
    publications: published
      .filter(p => p.year === year)
      .sort((a, b) => {
        const idA = parseInt(a.id.replace(/[^0-9]/g, ''))
        const idB = parseInt(b.id.replace(/[^0-9]/g, ''))
        return idB - idA
      })
  }))
})

// Conferences grouped by year (newest first)
const conferencesByYear = computed(() => {
  const years = [...new Set(filteredConferences.value.map(p => p.year))].sort((a, b) => b - a)
  return years.map(year => ({
    year,
    publications: filteredConferences.value
      .filter(p => p.year === year)
      .sort((a, b) => {
        const idA = parseInt(a.id.replace(/[^0-9]/g, ''))
        const idB = parseInt(b.id.replace(/[^0-9]/g, ''))
        return idB - idA
      })
  }))
})

</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-12">Publications</h1>

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
      </div>

      <!-- Member Filter -->
      <div class="flex justify-center mb-8 gap-2 flex-wrap">
        <button
          @click="selectedMember = null"
          class="px-4 py-1.5 rounded-full font-medium text-xs transition-colors shadow-sm"
          :class="!selectedMember ? 'bg-green-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'"
        >
          All
        </button>
        <button
          v-for="name in allMemberNames"
          :key="name"
          @click="selectedMember = name"
          class="px-4 py-1.5 rounded-full font-medium text-xs transition-colors shadow-sm"
          :class="selectedMember === name ? 'bg-green-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'"
        >
          {{ name }}
        </button>
      </div>

      <!-- Journals -->
      <div v-if="activeTab === 'journals'" class="space-y-8">
        <!-- In Submission Section -->
        <div v-if="inSubmission.length > 0">
          <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="bg-orange-500 text-white px-3 py-1 rounded-full mr-3 text-sm">In Submission</span>
            {{ inSubmission.length }} papers
          </h2>
          <div class="space-y-4">
            <div
              v-for="pub in inSubmission"
              :key="pub.id"
              class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow border-l-4 border-orange-400"
            >
              <div class="flex gap-4">
                <div class="flex-1">
                  <div class="flex items-start justify-between gap-2 mb-2">
                    <h3 class="font-medium text-gray-900">{{ pub.title }}</h3>
                    <span
                      v-if="selectedMember && getRoleBadge(getAuthorRole(pub, selectedMember))"
                      class="text-xs px-2 py-0.5 rounded-full whitespace-nowrap"
                      :class="getRoleBadge(getAuthorRole(pub, selectedMember))?.class"
                    >
                      {{ getRoleBadge(getAuthorRole(pub, selectedMember))?.text }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 mb-2">
                    <span v-for="(author, index) in pub.authors" :key="index">
                      <span :class="{ 'font-bold': author.includes('^') }">{{ author.replace(/[*+^]/g, '') }}</span><sup v-if="author.includes('+')" class="text-blue-600">†</sup><sup v-if="author.includes('*')" class="text-blue-600">*</sup><span v-if="index < pub.authors.length - 1">, </span>
                    </span>
                  </p>
                  <p class="text-sm">
                    <span class="text-blue-600 font-medium">{{ pub.journal }}</span>
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
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Published by Year -->
        <div v-for="yearGroup in publishedByYear" :key="yearGroup.year">
          <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="bg-blue-600 text-white px-3 py-1 rounded-full mr-3 text-sm">{{ yearGroup.year }}</span>
            {{ yearGroup.publications.length }} papers
          </h2>
          <div class="space-y-4">
            <div
              v-for="pub in yearGroup.publications"
              :key="pub.id"
              class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
            >
              <div class="flex gap-4">
                <!-- Highlight Image -->
                <div v-if="pub.highlightImage" class="flex-shrink-0 mr-2">
                  <img :src="getAssetUrl(pub.highlightImage)" :alt="pub.title" class="max-w-[12rem] max-h-[8rem] rounded-lg shadow-sm border border-gray-100 object-contain" />
                </div>

                <div class="flex-1">
                  <div class="flex items-start justify-between gap-2 mb-2">
                    <h3 class="font-medium text-gray-900">{{ pub.title }}</h3>
                    <span
                      v-if="selectedMember && getRoleBadge(getAuthorRole(pub, selectedMember))"
                      class="text-xs px-2 py-0.5 rounded-full whitespace-nowrap"
                      :class="getRoleBadge(getAuthorRole(pub, selectedMember))?.class"
                    >
                      {{ getRoleBadge(getAuthorRole(pub, selectedMember))?.text }}
                    </span>
                  </div>
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
                  <div v-if="pub.authors.some((a: string) => a.includes('+'))" class="flex gap-4 mt-3 text-xs text-gray-500 border-t pt-2">
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

      <!-- Conferences -->
      <div v-if="activeTab === 'conferences'" class="space-y-8">
        <div v-for="yearGroup in conferencesByYear" :key="yearGroup.year">
          <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="bg-blue-600 text-white px-3 py-1 rounded-full mr-3 text-sm">{{ yearGroup.year }}</span>
            {{ yearGroup.publications.length }} papers
          </h2>
          <div class="space-y-4">
            <div
              v-for="pub in yearGroup.publications"
              :key="pub.id"
              class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
            >
              <div class="flex-1">
                <div class="flex items-start justify-between gap-2 mb-2">
                  <h3 class="font-medium text-gray-900">{{ pub.title }}</h3>
                  <span
                    v-if="selectedMember && getRoleBadge(getAuthorRole(pub, selectedMember))"
                    class="text-xs px-2 py-0.5 rounded-full whitespace-nowrap"
                    :class="getRoleBadge(getAuthorRole(pub, selectedMember))?.class"
                  >
                    {{ getRoleBadge(getAuthorRole(pub, selectedMember))?.text }}
                  </span>
                </div>
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
                <div v-if="pub.authors.some((a: string) => a.includes('+'))" class="flex gap-4 mt-3 text-xs text-gray-500 border-t pt-2">
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
