<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="bg-gray-800 text-white mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Lab Info -->
        <div>
          <h3 class="text-lg font-semibold mb-4">UST AIMAT Lab</h3>
          <p class="text-gray-400 text-sm leading-relaxed">
            797 Changwon-daero, Seongsan-gu, Changwon-si<br>
            51508 Republic of Korea
          </p>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="text-lg font-semibold mb-4">Quick Links</h3>
          <ul class="space-y-2 text-sm">
            <li>
              <RouterLink to="/members" class="text-gray-400 hover:text-white transition-colors">
                Members
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/research" class="text-gray-400 hover:text-white transition-colors">
                Research Areas
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/achievements" class="text-gray-400 hover:text-white transition-colors">
                Publications
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/contact" class="text-gray-400 hover:text-white transition-colors">
                Contact
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Contact Info -->
        <div>
          <h3 class="text-lg font-semibold mb-4">Contact</h3>
          <ul class="space-y-2 text-sm text-gray-400">
            <li class="flex items-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>h.lee@kims.re.kr</span>
            </li>
            <li class="flex items-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <span>+82-55-280-3843</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Copyright -->
      <div class="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-400">
        <p>&copy; {{ currentYear }} UST AIMAT Lab. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>
