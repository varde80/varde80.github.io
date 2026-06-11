<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import logo from '@/assets/logo.png'

const isMenuOpen = ref(false)

const navItems = [
  { name: 'Home', path: '/' },
  { name: 'Members', path: '/members' },
  { name: 'Research Areas', path: '/research' },
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
  <header class="bg-navy-950/85 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
          <RouterLink to="/" class="flex items-center space-x-2 focus-ring rounded-md" @click="closeMenu">
            <img :src="logo" alt="UST Lab Logo" class="h-[48px] w-auto rounded bg-white/90 p-1" />
          </RouterLink>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex space-x-4 lg:space-x-6">
          <RouterLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="relative text-slate-300 hover:text-white px-2 py-2 text-sm font-medium transition-colors focus-ring rounded-md after:absolute after:left-2 after:right-2 after:-bottom-0.5 after:h-0.5 after:rounded-full after:bg-gradient-to-r after:from-brand-400 after:to-accent-400 after:opacity-0 after:transition-opacity"
            active-class="text-white after:opacity-100"
          >
            {{ item.name }}
          </RouterLink>
        </nav>

        <!-- Mobile Menu Button -->
        <button
          class="md:hidden p-2 rounded-md text-slate-300 hover:text-white hover:bg-white/10 focus-ring"
          @click="toggleMenu"
          aria-label="Toggle menu"
          :aria-expanded="isMenuOpen"
          aria-controls="mobile-nav"
        >
          <svg
            class="h-6 w-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
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
        id="mobile-nav"
        class="md:hidden pb-4"
      >
        <div class="flex flex-col space-y-2">
          <RouterLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="text-slate-300 hover:text-white hover:bg-white/10 px-3 py-2 rounded-md text-base font-medium transition-colors focus-ring"
            active-class="text-white bg-white/10"
            @click="closeMenu"
          >
            {{ item.name }}
          </RouterLink>
        </div>
      </nav>
    </div>
  </header>
</template>
