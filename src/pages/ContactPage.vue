<script setup lang="ts">
import { ref } from 'vue'
import contactData from '../data/contact.json'
import type { ContactInfo } from '../types'

const contact = ref<ContactInfo>(contactData as ContactInfo)
</script>

<template>
  <div class="py-12 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 text-center mb-12">Contact Us</h1>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Contact Information -->
        <div class="bg-white rounded-lg shadow-md p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Contact Information</h2>

          <div class="space-y-6">
            <!-- Address -->
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Address</h3>
                <p class="text-gray-600 whitespace-pre-line">{{ contact.address }}</p>
              </div>
            </div>

            <!-- Phone -->
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Phone</h3>
                <p class="text-gray-600">{{ contact.phone }}</p>
                <p v-if="contact.fax" class="text-gray-500 text-sm">FAX: {{ contact.fax }}</p>
              </div>
            </div>

            <!-- Email -->
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Email</h3>
                <a :href="`mailto:${contact.email}`" class="text-blue-600 hover:text-blue-800">
                  {{ contact.email }}
                </a>
              </div>
            </div>
          </div>

          <!-- Join Us -->
          <div class="mt-8 pt-8 border-t border-gray-200">
            <h3 class="font-semibold text-gray-900 mb-4">Join Our Lab</h3>
            <p class="text-gray-600 mb-4">
              We are looking for passionate and creative researchers to join our team.
              If you are interested in graduate studies or research positions, please contact us via email.
            </p>
            <p class="text-sm text-gray-500">
              Please attach your CV and transcripts when applying.
            </p>
          </div>
        </div>

        <!-- Map -->
        <div class="bg-white rounded-lg shadow-md overflow-hidden h-[500px]">
          <iframe
            v-if="contact.mapCoordinates"
            width="100%"
            height="100%"
            frameborder="0"
            scrolling="no"
            marginheight="0"
            marginwidth="0"
            :src="`https://maps.google.com/maps?q=${contact.mapCoordinates.lat},${contact.mapCoordinates.lng}&z=15&output=embed`"
            class="w-full h-full"
          ></iframe>
          <div v-else class="h-full bg-gray-200 flex items-center justify-center">
            <p class="text-gray-500">Map coordinates not available</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
