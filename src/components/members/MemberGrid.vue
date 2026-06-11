<script setup lang="ts">
import type { Member } from '../../types'
import MemberCard from './MemberCard.vue'

defineProps<{
  title: string
  members: Member[]
}>()
</script>

<template>
  <section v-if="members.length > 0" class="mb-16">
    <h2 class="text-2xl font-bold text-gray-800 mb-8 flex items-center gap-3 border-b border-gray-200 pb-2">
      <span aria-hidden="true" class="w-1.5 h-6 rounded bg-gradient-to-b from-brand-500 to-accent-500"></span>
      {{ title }}
    </h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6">
      <MemberCard v-for="member in members" :key="member.id" :member="member" />
    </div>
  </section>
</template>
