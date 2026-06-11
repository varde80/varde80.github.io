import { computed, onMounted, onUnmounted, readonly, ref, toValue, type MaybeRefOrGetter, type Ref } from 'vue'

export interface UseCarouselOptions {
  /** Number of slides; may be reactive. */
  length: MaybeRefOrGetter<number>
  /** Autoplay interval in ms. */
  interval?: number
  /** Autoplay on mount; force-disabled when the user prefers reduced motion. */
  autoplay?: boolean
}

export interface UseCarouselReturn {
  current: Ref<number>
  next: () => void
  prev: () => void
  goTo: (index: number) => void
  pause: () => void
  resume: () => void
  isPaused: Readonly<Ref<boolean>>
}

export function useCarousel(options: UseCarouselOptions): UseCarouselReturn {
  const { interval = 5000, autoplay = true } = options
  const length = computed(() => toValue(options.length))

  const current = ref(0)
  const isPaused = ref(false)
  let timer: ReturnType<typeof setInterval> | null = null

  const prefersReducedMotion = () =>
    typeof window !== 'undefined' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches

  const stopTimer = () => {
    if (timer !== null) {
      clearInterval(timer)
      timer = null
    }
  }

  const startTimer = () => {
    stopTimer()
    if (!autoplay || prefersReducedMotion() || length.value <= 1) return
    timer = setInterval(() => {
      if (!isPaused.value) {
        current.value = (current.value + 1) % length.value
      }
    }, interval)
  }

  const next = () => {
    if (length.value === 0) return
    current.value = (current.value + 1) % length.value
    startTimer()
  }

  const prev = () => {
    if (length.value === 0) return
    current.value = (current.value - 1 + length.value) % length.value
    startTimer()
  }

  const goTo = (index: number) => {
    if (length.value === 0) return
    current.value = ((index % length.value) + length.value) % length.value
    startTimer()
  }

  const pause = () => {
    isPaused.value = true
  }

  const resume = () => {
    isPaused.value = false
  }

  onMounted(startTimer)
  onUnmounted(stopTimer)

  return { current, next, prev, goTo, pause, resume, isPaused: readonly(isPaused) }
}
