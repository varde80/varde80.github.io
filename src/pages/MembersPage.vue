<script setup lang="ts">
import { ref } from 'vue'
import membersData from '../data/members.json'
import professorData from '../data/professor.json'
import type { MembersData, Professor } from '../types'
import { getAssetUrl } from '../utils/assets'
import PageHero from '../components/common/PageHero.vue'
import FilterPill from '../components/ui/FilterPill.vue'
import MemberGrid from '../components/members/MemberGrid.vue'

const members = ref<MembersData>(membersData as MembersData)
const professor = ref<Professor>(professorData as Professor)
const showEmail = ref(false)
const activeTab = ref<'professor' | 'members'>('professor')
</script>

<template>
  <div class="bg-gray-50 min-h-screen">
    <PageHero title="Members" subtitle="The people behind AIMAT Lab's research.">
      <div class="flex flex-wrap mt-8 gap-4">
        <FilterPill :active="activeTab === 'professor'" @click="activeTab = 'professor'">
          Professor
        </FilterPill>
        <FilterPill :active="activeTab === 'members'" @click="activeTab = 'members'">
          Lab Members
        </FilterPill>
      </div>
    </PageHero>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Professor Tab -->
      <div v-if="activeTab === 'professor'">
        <section class="mb-16">
          <div class="glass-card p-6 md:p-8">
            <div class="flex flex-col md:flex-row gap-8">
              <div class="flex-shrink-0">
                <div class="w-48 h-48 bg-gray-200 rounded-lg overflow-hidden">
                  <img :src="getAssetUrl(professor.image)" :alt="professor.name" class="w-full h-full object-cover" />
                </div>
              </div>
              <div class="flex-1">
                <h3 class="text-2xl font-bold text-gray-900">{{ professor.name }}</h3>
                <p class="text-brand-600 font-medium mb-4">{{ professor.title }}</p>

                <div class="space-y-2 text-sm text-gray-700 mb-4">
                  <p class="flex items-center">
                    <button
                      @click="showEmail = !showEmail"
                      class="flex items-center hover:text-brand-600 transition-colors cursor-pointer focus-ring rounded"
                      :aria-pressed="showEmail"
                      :title="showEmail ? 'Hide email' : 'Show email'"
                    >
                      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                      <span v-if="showEmail">{{ professor.email }}</span>
                      <span v-else class="text-gray-400">Click to show email</span>
                    </button>
                  </p>
                  <p v-if="professor.phone" class="flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                    {{ professor.phone }}
                  </p>
                </div>

                <div class="space-y-6">
                  <!-- Education -->
                  <div>
                    <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
                      <span aria-hidden="true" class="w-1 h-5 rounded mr-2 bg-gradient-to-b from-brand-500 to-accent-500"></span>
                      Education
                    </h4>
                    <ul class="text-sm text-gray-600 space-y-3 ml-3">
                      <li v-for="(edu, index) in professor.education" :key="index">
                        <div class="flex">
                          <span class="text-brand-400 mr-2">•</span>
                          <div>
                            <span class="font-medium text-gray-900">{{ edu.degree }}, {{ edu.field }}</span>
                            <span class="text-gray-600">, {{ edu.institution }}, {{ edu.period }}</span>
                            <div v-if="edu.thesis" class="text-gray-500 text-xs mt-1 ml-8">
                              {{ edu.thesis }}
                              <span v-if="edu.advisor">({{ edu.advisor }})</span>
                            </div>
                          </div>
                        </div>
                      </li>
                    </ul>
                  </div>

                  <!-- Experience -->
                  <div>
                    <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
                      <span aria-hidden="true" class="w-1 h-5 rounded mr-2 bg-gradient-to-b from-brand-500 to-accent-500"></span>
                      Experience
                    </h4>
                    <ul class="text-sm space-y-2 ml-3">
                      <li v-for="(exp, index) in professor.experience" :key="index" class="flex">
                        <span :class="exp.period.includes('Present') ? 'text-brand-600' : 'text-brand-400'" class="mr-2">•</span>
                        <span :class="exp.period.includes('Present') ? 'text-gray-900 font-medium' : 'text-gray-600'">
                          {{ exp.period }}, {{ exp.position }}, {{ exp.Department ? exp.Department + ', ' : '' }}{{ exp.institution }}
                        </span>
                      </li>
                    </ul>
                  </div>

                  <!-- Grants and Awards -->
                  <div v-if="professor['Grants and Awards']">
                    <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
                      <span aria-hidden="true" class="w-1 h-5 rounded mr-2 bg-gradient-to-b from-brand-500 to-accent-500"></span>
                      Grants and Awards
                    </h4>
                    <ul class="text-sm text-gray-600 space-y-2 ml-3">
                      <li v-for="(award, index) in professor['Grants and Awards']" :key="index" class="flex">
                        <span class="text-brand-400 mr-2">•</span>
                        <span>{{ award }}</span>
                      </li>
                    </ul>
                  </div>

                  <!-- Professional Activities -->
                  <div v-if="professor['Professional Activities/Memberships']">
                    <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
                      <span aria-hidden="true" class="w-1 h-5 rounded mr-2 bg-gradient-to-b from-brand-500 to-accent-500"></span>
                      Professional Activities
                    </h4>
                    <ul class="text-sm text-gray-600 space-y-2 ml-3">
                      <li v-for="(activity, index) in professor['Professional Activities/Memberships']" :key="index" class="flex">
                        <span class="text-brand-400 mr-2">•</span>
                        <span>{{ activity }}</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Members Tab -->
      <div v-if="activeTab === 'members'">
        <MemberGrid title="Postdoctoral Researchers" :members="members.researchers" />
        <MemberGrid title="Ph.D. Students" :members="members.phdStudents" />
        <MemberGrid title="M.S. Students" :members="members.msStudents" />
        <MemberGrid title="Intern" :members="members.Intern" />

        <!-- Alumni -->
        <section v-if="members.alumni.length > 0">
          <h2 class="text-2xl font-bold text-gray-800 mb-8 flex items-center gap-3 border-b border-gray-200 pb-2">
            <span aria-hidden="true" class="w-1.5 h-6 rounded bg-gradient-to-b from-brand-500 to-accent-500"></span>
            Alumni
          </h2>
          <div class="glass-card overflow-hidden">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50/80">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Degree</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current Position</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr v-for="alum in members.alumni" :key="alum.id" class="hover:bg-gray-50/60">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="font-medium text-gray-900">{{ alum.name }}</div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-600">{{ alum.position }}</td>
                    <td class="px-6 py-4 text-sm text-gray-600">{{ alum.research }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
