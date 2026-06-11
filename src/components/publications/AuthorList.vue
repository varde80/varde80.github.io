<script setup lang="ts">
// Author marker conventions: ^ lab member (bold), + equal contribution (†),
// * corresponding author.
defineProps<{
  authors: string[]
}>()
</script>

<template>
  <p class="text-sm text-gray-600">
    <span v-for="(author, index) in authors" :key="index">
      <span :class="{ 'font-bold': author.includes('^') }">{{ author.replace(/[*+^]/g, '') }}</span><sup v-if="author.includes('+')" class="text-brand-600">†</sup><sup v-if="author.includes('*')" class="text-brand-600">*</sup><span v-if="index < authors.length - 1">, </span>
    </span>
  </p>
</template>
