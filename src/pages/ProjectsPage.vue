<script setup lang="ts">
import { ref, computed } from 'vue'
import projectsData from '../data/projects.json'
import type { Project } from '../types'

const projects = ref<Project[]>(projectsData as Project[])
const sortBy = ref<'year' | 'role'>('year')

const getFieldValue = (field: any, lang: 'en' | 'ko' = 'en') => {
  if (typeof field === 'string') return field
  if (field && typeof field === 'object') return field[lang] || field.en || field.ko || ''
  return ''
}

const getRolePriority = (role: any) => {
  const roleEn = getFieldValue(role, 'en').toUpperCase()
  if (roleEn === 'PI') return 1
  if (roleEn === 'CO-PI') return 2
  if (roleEn === 'CO-INVESTIGATOR') return 3
  return 4 // Participant
}

const getStartYear = (period: any) => {
  const periodStr = getFieldValue(period, 'en')
  const match = periodStr.match(/(\d{4})/)
  return match ? parseInt(match[1]) : 0
}

const sortProjects = (projectList: Project[]) => {
  return [...projectList].sort((a, b) => {
    if (sortBy.value === 'year') {
      return getStartYear(b.period) - getStartYear(a.period) // 최신순
    } else {
      const roleDiff = getRolePriority(a.role) - getRolePriority(b.role)
      if (roleDiff !== 0) return roleDiff
      return getStartYear(b.period) - getStartYear(a.period) // 같은 역할이면 최신순
    }
  })
}

const ongoingProjects = computed(() => {
  return sortProjects(projects.value.filter(p => p.status === 'ongoing'))
})

const completedProjects = computed(() => {
  return sortProjects(projects.value.filter(p => p.status === 'completed'))
})

const getRoleBadgeClass = (role: any) => {
  const roleEn = getFieldValue(role, 'en').toUpperCase()
  if (roleEn === 'PI') return 'bg-orange-500 text-white'
  if (roleEn === 'CO-PI') return 'bg-blue-500 text-white'
  return 'bg-gray-500 text-white'
}
</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-4">Projects</h1>
      <p class="text-lg text-gray-600 text-center mb-8">Research projects in our lab.</p>

      <!-- Sort Options -->
      <div class="flex justify-end gap-2 mb-8">
        <span class="text-sm text-gray-500 mr-2 self-center">Sort by:</span>
        <button
          @click="sortBy = 'year'"
          class="px-4 py-1.5 rounded-full text-sm font-medium transition-colors"
          :class="sortBy === 'year' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100 shadow-sm'"
        >
          Year
        </button>
        <button
          @click="sortBy = 'role'"
          class="px-4 py-1.5 rounded-full text-sm font-medium transition-colors"
          :class="sortBy === 'role' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100 shadow-sm'"
        >
          Role
        </button>
      </div>

      <!-- Ongoing Projects -->
      <div v-if="ongoingProjects.length > 0" class="mb-12">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <span class="bg-green-600 text-white px-3 py-1 rounded-full mr-3 text-sm">Ongoing</span>
          {{ ongoingProjects.length }} Projects
        </h2>
        <div class="space-y-6">
          <div
            v-for="project in ongoingProjects"
            :key="project.id"
            class="bg-white rounded-lg shadow-md overflow-hidden border-l-4 border-green-500"
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
                <div>
                  <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Period</p>
                  <p class="text-gray-800 font-medium">{{ getFieldValue(project.period, 'en') }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Funding Agency</p>
                  <p class="text-gray-800 font-medium">{{ getFieldValue(project.fundingAgency, 'en') }}</p>
                </div>
                <div v-if="project.fundingAmount">
                  <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Budget</p>
                  <p class="text-gray-800 font-medium">{{ getFieldValue(project.fundingAmount, 'en') }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Completed Projects -->
      <div v-if="completedProjects.length > 0">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <span class="bg-gray-500 text-white px-3 py-1 rounded-full mr-3 text-sm">Completed</span>
          {{ completedProjects.length }} Projects
        </h2>
        <div class="space-y-6">
          <div
            v-for="project in completedProjects"
            :key="project.id"
            class="bg-white rounded-lg shadow-md overflow-hidden border-l-4 border-gray-400"
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
                <div>
                  <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Period</p>
                  <p class="text-gray-800 font-medium">{{ getFieldValue(project.period, 'en') }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Funding Agency</p>
                  <p class="text-gray-800 font-medium">{{ getFieldValue(project.fundingAgency, 'en') }}</p>
                </div>
                <div v-if="project.fundingAmount">
                  <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Budget</p>
                  <p class="text-gray-800 font-medium">{{ getFieldValue(project.fundingAmount, 'en') }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="projects.length === 0" class="text-center py-12">
        <p class="text-gray-500">No projects available yet.</p>
      </div>
    </div>
  </div>
</template>
