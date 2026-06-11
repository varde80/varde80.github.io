<script setup lang="ts">
import type { Member } from '../../types'
import { getAssetUrl } from '../../utils/assets'

defineProps<{
  member: Member
}>()
</script>

<template>
  <div class="glass-card card-lift overflow-hidden">
    <div class="h-52 bg-gray-100 flex items-center justify-center overflow-hidden">
      <img
        :src="getAssetUrl(member.image)"
        :alt="member.name"
        class="max-h-full max-w-full object-contain"
      />
    </div>
    <div class="p-4">
      <h3 class="font-semibold text-gray-900">{{ member.name }}</h3>
      <p class="text-sm text-brand-600 mt-1">{{ member.position }}</p>
      <p v-if="member.research" class="text-sm text-gray-600 mt-2">{{ member.research }}</p>
    </div>
  </div>
</template>
