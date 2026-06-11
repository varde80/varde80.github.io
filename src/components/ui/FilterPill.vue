<script setup lang="ts">
withDefaults(
  defineProps<{
    active: boolean
    size?: 'sm' | 'md'
  }>(),
  { size: 'md' }
)

const emit = defineEmits<{
  click: []
}>()
</script>

<template>
  <button
    type="button"
    :aria-pressed="active"
    class="rounded-full font-medium transition-colors shadow-sm focus-ring"
    :class="[
      size === 'sm' ? 'px-4 py-1.5 text-xs' : 'px-6 py-2 text-sm',
      active
        ? 'bg-gradient-to-r from-brand-600 to-accent-600 text-white'
        : 'bg-white/90 text-gray-600 hover:bg-gray-50'
    ]"
    @click="emit('click')"
  >
    <slot />
  </button>
</template>
