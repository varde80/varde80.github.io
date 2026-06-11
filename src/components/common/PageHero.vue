<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
}>()
</script>

<template>
  <section class="relative overflow-hidden bg-navy-950">
    <!-- Accent glow blobs -->
    <div aria-hidden="true" class="pointer-events-none absolute inset-0">
      <div class="absolute -top-24 -left-24 h-72 w-72 rounded-full bg-brand-600/20 blur-3xl"></div>
      <div class="absolute -bottom-32 right-0 h-80 w-80 rounded-full bg-accent-600/20 blur-3xl"></div>
    </div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 sm:py-16">
      <h1 class="text-3xl sm:text-4xl font-bold gradient-text">{{ title }}</h1>
      <p v-if="subtitle" class="mt-3 max-w-3xl text-base sm:text-lg text-slate-300">
        {{ subtitle }}
      </p>
      <slot />
    </div>
  </section>
</template>
