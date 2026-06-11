<script setup lang="ts">
import { ref, computed } from 'vue'
import projectsData from '../data/projects.json'
import type { Project } from '../types'
import { localize } from '../utils/i18n'
import PageHero from '../components/common/PageHero.vue'
import FilterPill from '../components/ui/FilterPill.vue'
import BaseBadge from '../components/ui/BaseBadge.vue'
import ProjectCard from '../components/projects/ProjectCard.vue'

const projects = ref<Project[]>(projectsData as Project[])
const sortBy = ref<'year' | 'role'>('year')

const getRolePriority = (role: Project['role']) => {
  const roleEn = localize(role, 'en').toUpperCase()
  if (roleEn === 'PI') return 1
  if (roleEn === 'CO-PI') return 2
  if (roleEn === 'CO-INVESTIGATOR') return 3
  return 4 // Participant
}

const getStartYear = (period: Project['period']) => {
  const match = localize(period, 'en').match(/\d{4}/)
  return match ? parseInt(match[0]) : 0
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
</script>

<template>
  <div class="bg-gray-50 min-h-screen">
    <PageHero title="Projects" subtitle="Research projects in our lab." />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Sort Options -->
      <div class="flex justify-end gap-2 mb-8">
        <span class="text-sm text-gray-500 mr-2 self-center">Sort by:</span>
        <FilterPill size="sm" :active="sortBy === 'year'" @click="sortBy = 'year'">
          Year
        </FilterPill>
        <FilterPill size="sm" :active="sortBy === 'role'" @click="sortBy = 'role'">
          Role
        </FilterPill>
      </div>

      <!-- Ongoing Projects -->
      <div v-if="ongoingProjects.length > 0" class="mb-12">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-3">
          <BaseBadge variant="solid-gradient" size="md">Ongoing</BaseBadge>
          {{ ongoingProjects.length }} Projects
        </h2>
        <div class="space-y-6">
          <ProjectCard v-for="project in ongoingProjects" :key="project.id" :project="project" />
        </div>
      </div>

      <!-- Completed Projects -->
      <div v-if="completedProjects.length > 0">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-3">
          <BaseBadge variant="soft-gray" size="md">Completed</BaseBadge>
          {{ completedProjects.length }} Projects
        </h2>
        <div class="space-y-6">
          <ProjectCard v-for="project in completedProjects" :key="project.id" :project="project" />
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="projects.length === 0" class="text-center py-12">
        <p class="text-gray-500">No projects available yet.</p>
      </div>
    </div>
  </div>
</template>
