<script setup lang="ts">
import { ref, computed } from 'vue'
import projectsData from '../data/projects.json'
import type { Project } from '../types'

const projects = ref<Project[]>(projectsData as Project[])
const activeTab = ref<'ongoing' | 'completed'>('ongoing')

const ongoingProjects = computed(() => {
  return projects.value.filter(p => p.status === 'ongoing')
})

const completedProjects = computed(() => {
  return projects.value.filter(p => p.status === 'completed')
})

const filteredProjects = computed(() => {
  return activeTab.value === 'ongoing' ? ongoingProjects.value : completedProjects.value
})

const getFieldValue = (field: any, lang: 'en' | 'ko' = 'en') => {
  if (typeof field === 'string') return field
  if (field && typeof field === 'object') return field[lang] || field.en || field.ko || ''
  return ''
}

const getRoleBadgeClass = (role: any) => {
  const roleEn = getFieldValue(role, 'en').toUpperCase()
  if (roleEn === 'PI') return 'bg-blue-600 text-white'
  if (roleEn === 'CO-PI') return 'bg-blue-500 text-white'
  return 'bg-gray-500 text-white'
}
</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-4">Projects</h1>
      <p class="text-lg text-gray-600 text-center mb-8">Research projects in our lab.</p>

      <!-- Tabs -->
      <div class="flex justify-center mb-8 gap-4">
        <button
          @click="activeTab = 'ongoing'"
          class="px-6 py-2 rounded-full font-medium text-sm transition-colors shadow-sm"
          :class="activeTab === 'ongoing' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'"
        >
          Ongoing ({{ ongoingProjects.length }})
        </button>
        <button
          @click="activeTab = 'completed'"
          class="px-6 py-2 rounded-full font-medium text-sm transition-colors shadow-sm"
          :class="activeTab === 'completed' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'"
        >
          Completed ({{ completedProjects.length }})
        </button>
      </div>

      <!-- Projects List -->
      <div class="space-y-6">
        <div
          v-for="project in filteredProjects"
          :key="project.id"
          class="bg-white rounded-lg shadow-md overflow-hidden"
        >
          <div class="p-6">
            <!-- Header with Title and Role Badge -->
            <div class="flex flex-wrap items-start justify-between gap-3 mb-4">
              <div class="flex-1">
                <h3 class="text-xl font-bold text-gray-900">{{ getFieldValue(project.title, 'en') }}</h3>
                <p class="text-lg text-gray-600">{{ getFieldValue(project.title, 'ko') }}</p>
              </div>
              <span
                class="px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap"
                :class="getRoleBadgeClass(project.role)"
              >
                {{ getFieldValue(project.role, 'en') }}
              </span>
            </div>

            <!-- Project Details -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-100">
              <!-- Period -->
              <div>
                <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Period</p>
                <p class="text-gray-800 font-medium">{{ getFieldValue(project.period, 'en') }}</p>
              </div>

              <!-- Funding Agency -->
              <div>
                <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Funding Agency</p>
                <p class="text-gray-800 font-medium">{{ getFieldValue(project.fundingAgency, 'en') }}</p>
              </div>

              <!-- Funding Amount -->
              <div v-if="project.fundingAmount">
                <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Budget</p>
                <p class="text-gray-800 font-medium">{{ getFieldValue(project.fundingAmount, 'en') }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredProjects.length === 0" class="text-center py-12">
        <p class="text-gray-500">No {{ activeTab }} projects available.</p>
      </div>
    </div>
  </div>
</template>
