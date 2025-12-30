<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import logo from '@/assets/logo.png'

const isMenuOpen = ref(false)

const navItems = [
  { name: 'Home', path: '/' },
  { name: 'Members', path: '/members' },
  { name: 'Research', path: '/research' },
  { name: 'Projects', path: '/projects' },
  { name: 'Facilities', path: '/facilities' },
  { name: 'Publications', path: '/achievements' },
  { name: 'Software', path: '/software' },
  { name: 'News', path: '/news' },
  { name: 'Contact', path: '/contact' }
]

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<template>
  <header class="bg-white shadow-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
          <RouterLink to="/" class="flex items-center space-x-2" @click="closeMenu">
            <img :src="logo" alt="UST Lab Logo" class="h-[48px] w-auto" />
          </RouterLink>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex space-x-8">
          <RouterLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors"
            active-class="text-blue-600 border-b-2 border-blue-600"
          >
            {{ item.name }}
          </RouterLink>
        </nav>

        <!-- Mobile Menu Button -->
        <button
          class="md:hidden p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-100"
          @click="toggleMenu"
          aria-label="Toggle menu"
        >
          <svg
            class="h-6 w-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              v-if="!isMenuOpen"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Mobile Navigation -->
      <nav
        v-show="isMenuOpen"
        class="md:hidden pb-4"
      >
        <div class="flex flex-col space-y-2">
          <RouterLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium transition-colors"
            active-class="text-blue-600 bg-blue-50"
            @click="closeMenu"
          >
            {{ item.name }}
          </RouterLink>
        </div>
      </nav>
    </div>
  </header>
</template>
