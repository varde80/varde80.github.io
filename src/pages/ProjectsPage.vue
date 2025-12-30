<script setup lang="ts">
import { ref, computed } from 'vue'
import projectsData from '../data/projects.json'
import type { Project } from '../types'

const projects = ref<Project[]>(projectsData as Project[])

const sortedProjects = computed(() => {
  return [...projects.value].sort((a, b) => {
    if (a.status === 'ongoing' && b.status === 'completed') return -1
    if (a.status === 'completed' && b.status === 'ongoing') return 1
    return 0
  })
})
</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-4">Projects</h1>
      <p class="text-lg text-gray-600 text-center mb-12">Research projects in our lab.</p>

      <!-- Projects List -->
      <div class="space-y-6">
        <div
          v-for="project in sortedProjects"
          :key="project.id"
          class="bg-white rounded-lg shadow-md overflow-hidden"
        >
          <div class="p-6">
            <!-- Header with Title and Status Badge -->
            <div class="flex flex-wrap items-start justify-between gap-3 mb-4">
              <div>
                <h3 class="text-xl font-bold text-gray-900">{{ project.title.en }}</h3>
                <p class="text-lg text-gray-600">{{ project.title.ko }}</p>
              </div>
              <span
                class="px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap"
                :class="project.status === 'ongoing'
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-600'"
              >
                {{ project.status === 'ongoing' ? 'Ongoing' : 'Completed' }}
              </span>
            </div>

            <!-- Description -->
            <div class="mb-4">
              <p class="text-gray-700">{{ project.description.en }}</p>
              <p class="text-gray-500 text-sm mt-1">{{ project.description.ko }}</p>
            </div>

            <!-- Project Details -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-100">
              <!-- Period -->
              <div>
                <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Period / 연구기간</p>
                <p class="text-gray-800 font-medium">{{ project.period.en }}</p>
                <p class="text-gray-500 text-sm">{{ project.period.ko }}</p>
              </div>

              <!-- Role -->
              <div>
                <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Role / 역할</p>
                <p class="text-gray-800 font-medium">{{ project.role.en }}</p>
                <p class="text-gray-500 text-sm">{{ project.role.ko }}</p>
              </div>

              <!-- Funding Agency -->
              <div>
                <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Funding / 펀딩기관</p>
                <p class="text-gray-800 font-medium">{{ project.fundingAgency.en }}</p>
                <p class="text-gray-500 text-sm">{{ project.fundingAgency.ko }}</p>
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
