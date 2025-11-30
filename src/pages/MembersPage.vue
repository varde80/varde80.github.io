<script setup lang="ts">
import { ref } from 'vue'
import membersData from '../data/members.json'
import type { MembersData } from '../types'
import { getAssetUrl } from '../utils/assets'

const members = ref<MembersData>(membersData as MembersData)
const showEmail = ref(false)
</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-12">Members</h1>

      <!-- Professor -->
      <section class="mb-16">
        <h2 class="text-2xl font-bold text-gray-800 mb-8 border-b-2 border-blue-600 pb-2">Professor</h2>
        <div class="bg-white rounded-lg shadow-md p-6 md:p-8">
          <div class="flex flex-col md:flex-row gap-8">
            <div class="flex-shrink-0">
              <div class="w-48 h-48 bg-gray-200 rounded-lg overflow-hidden">
                <img :src="getAssetUrl(members.professor.image)" :alt="members.professor.name" class="w-full h-full object-cover" />
              </div>
            </div>
            <div class="flex-1">
              <h3 class="text-2xl font-bold text-gray-900">{{ members.professor.name }}</h3>
              <p class="text-blue-600 font-medium mb-4">{{ members.professor.title }}</p>

              <div class="space-y-2 text-sm text-gray-700 mb-4">
                <p class="flex items-center">
                  <button
                    @click="showEmail = !showEmail"
                    class="flex items-center hover:text-blue-600 transition-colors cursor-pointer"
                    :title="showEmail ? 'Hide email' : 'Show email'"
                  >
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    <span v-if="showEmail">{{ members.professor.email }}</span>
                    <span v-else class="text-gray-400">Click to show email</span>
                  </button>
                </p>
                <p v-if="members.professor.phone" class="flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  {{ members.professor.phone }}
                </p>
              </div>

              <p class="text-gray-700 mb-6">{{ members.professor.bio }}</p>

              <div class="flex flex-col md:flex-row gap-6">
                <div class="md:w-[35%]">
                  <h4 class="font-semibold text-gray-900 mb-2">Education</h4>
                  <ul class="text-sm text-gray-600 space-y-1">
                    <li v-for="(edu, index) in members.professor.education" :key="index">{{ edu }}</li>
                  </ul>
                </div>
                <div class="md:w-[65%]">
                  <h4 class="font-semibold text-gray-900 mb-2">Experience</h4>
                  <ul class="text-sm text-gray-600 space-y-1">
                    <li v-for="(exp, index) in members.professor.experience" :key="index">{{ exp }}</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Researchers -->
      <section v-if="members.researchers.length > 0" class="mb-16">
        <h2 class="text-2xl font-bold text-gray-800 mb-8 border-b-2 border-blue-600 pb-2">Researchers</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="member in members.researchers"
            :key="member.id"
            class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div class="h-80 bg-gray-100 flex items-center justify-center">
              <img :src="getAssetUrl(member.image)" :alt="member.name" class="h-full object-contain" />
            </div>
            <div class="p-4">
              <h3 class="font-semibold text-gray-900">{{ member.name }}</h3>
              <p class="text-sm text-blue-600 mt-1">{{ member.position }}</p>
              <p v-if="member.research" class="text-sm text-gray-600 mt-2">{{ member.research }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Ph.D. Students -->
      <section v-if="members.phdStudents.length > 0" class="mb-16">
        <h2 class="text-2xl font-bold text-gray-800 mb-8 border-b-2 border-blue-600 pb-2">Ph.D. Students</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="member in members.phdStudents"
            :key="member.id"
            class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div class="h-60 bg-gray-100 flex items-center justify-center">
              <img :src="getAssetUrl(member.image)" :alt="member.name" class="h-full object-contain" />
            </div>
            <div class="p-4">
              <h3 class="font-semibold text-gray-900">{{ member.name }}</h3>
              <p class="text-sm text-blue-600 mt-1">{{ member.position }}</p>
              <p v-if="member.research" class="text-sm text-gray-600 mt-2">{{ member.research }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- M.S. Students -->
      <section v-if="members.msStudents.length > 0" class="mb-16">
        <h2 class="text-2xl font-bold text-gray-800 mb-8 border-b-2 border-blue-600 pb-2">M.S. Students</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="member in members.msStudents"
            :key="member.id"
            class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div class="h-60 bg-gray-100 flex items-center justify-center">
              <img :src="getAssetUrl(member.image)" :alt="member.name" class="h-full object-contain" />
            </div>
            <div class="p-4">
              <h3 class="font-semibold text-gray-900">{{ member.name }}</h3>
              <p class="text-sm text-blue-600 mt-1">{{ member.position }}</p>
              <p v-if="member.research" class="text-sm text-gray-600 mt-2">{{ member.research }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Alumni -->
      <section v-if="members.alumni.length > 0">
        <h2 class="text-2xl font-bold text-gray-800 mb-8 border-b-2 border-blue-600 pb-2">Alumni</h2>
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Degree</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current Position</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="alum in members.alumni" :key="alum.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="font-medium text-gray-900">{{ alum.name }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ alum.position }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ alum.research }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>
