<script setup lang="ts">
import type { BadgeVariant } from '../../types'

withDefaults(
  defineProps<{
    variant: BadgeVariant
    size?: 'sm' | 'md'
  }>(),
  { size: 'sm' }
)

// Complete literal class strings so the Tailwind scanner picks them up
const variantClasses: Record<BadgeVariant, string> = {
  'solid-warning': 'bg-highlight-500 text-white',
  'solid-accent': 'bg-accent-500 text-white',
  'solid-gradient': 'bg-gradient-to-r from-brand-600 to-accent-600 text-white',
  'soft-purple': 'bg-accent-100 text-accent-700',
  'soft-green': 'bg-green-100 text-green-700',
  'soft-gray': 'bg-gray-100 text-gray-600',
  'soft-indigo': 'bg-indigo-100 text-indigo-700',
  'soft-emerald': 'bg-emerald-100 text-emerald-700'
}

const sizeClasses: Record<'sm' | 'md', string> = {
  sm: 'text-xs px-2 py-0.5',
  md: 'text-sm px-3 py-1'
}
</script>

<template>
  <span
    class="rounded-full font-medium inline-flex items-center"
    :class="[variantClasses[variant], sizeClasses[size]]"
  >
    <slot />
  </span>
</template>
