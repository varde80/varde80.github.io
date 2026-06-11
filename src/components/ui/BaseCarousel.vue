<script setup lang="ts" generic="T">
import { computed, watch } from 'vue'
import { useCarousel } from '../../composables/useCarousel'

const props = withDefaults(
  defineProps<{
    slides: T[]
    interval?: number
    label: string
    /** Position of the dot indicators. */
    dots?: 'center' | 'right'
  }>(),
  { interval: 5000, dots: 'center' }
)

const emit = defineEmits<{
  change: [index: number]
}>()

const { current, next, prev, goTo, pause, resume } = useCarousel({
  length: () => props.slides.length,
  interval: props.interval
})

watch(current, index => emit('change', index))

const showControls = computed(() => props.slides.length > 1)

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'ArrowLeft') {
    e.preventDefault()
    prev()
  } else if (e.key === 'ArrowRight') {
    e.preventDefault()
    next()
  }
}
</script>

<template>
  <div
    role="region"
    aria-roledescription="carousel"
    :aria-label="label"
    tabindex="0"
    class="relative h-full w-full focus-ring"
    @keydown="onKeydown"
    @mouseenter="pause"
    @mouseleave="resume"
    @focusin="pause"
    @focusout="resume"
  >
    <div
      v-for="(slide, index) in slides"
      :key="index"
      class="absolute inset-0 transition-opacity duration-1000"
      :class="current === index ? 'opacity-100' : 'opacity-0 pointer-events-none'"
      :aria-hidden="current !== index"
    >
      <slot name="slide" :slide="slide" :index="index" :active="current === index" />
    </div>

    <template v-if="showControls">
      <button
        @click="prev"
        aria-label="Previous slide"
        class="absolute left-4 top-1/2 -translate-y-1/2 z-10 bg-white/20 hover:bg-white/40 text-white p-2 rounded-full transition-colors focus-ring"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <button
        @click="next"
        aria-label="Next slide"
        class="absolute right-4 top-1/2 -translate-y-1/2 z-10 bg-white/20 hover:bg-white/40 text-white p-2 rounded-full transition-colors focus-ring"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <div
        class="absolute bottom-4 z-10 flex space-x-2"
        :class="dots === 'right' ? 'right-4' : 'left-1/2 -translate-x-1/2'"
      >
        <button
          v-for="(_, index) in slides"
          :key="index"
          @click="goTo(index)"
          :aria-label="`Go to slide ${index + 1}`"
          :aria-current="current === index"
          class="w-3 h-3 rounded-full transition-colors focus-ring"
          :class="current === index ? 'bg-white' : 'bg-white/50 hover:bg-white/70'"
        ></button>
      </div>
    </template>
  </div>
</template>
