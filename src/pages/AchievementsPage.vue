<script setup lang="ts">
import { ref, computed } from 'vue'
import journalsData from '../data/journals.json'
import preprintsData from '../data/preprints.json'
import conferencesData from '../data/conferences.json'
import membersData from '../data/members.json'
import professorData from '../data/professor.json'
import IFData from '../data/IF.json'
import type { Publication, MembersData, Professor, RoleBadge } from '../types'
import PageHero from '../components/common/PageHero.vue'
import FilterPill from '../components/ui/FilterPill.vue'
import BaseBadge from '../components/ui/BaseBadge.vue'
import PublicationCard from '../components/publications/PublicationCard.vue'

const journals = ref<Publication[]>(journalsData as Publication[])
const preprints = ref<Publication[]>(preprintsData as Publication[])
const conferences = ref<Publication[]>(conferencesData as Publication[])
const members = membersData as MembersData
const professor = professorData as Professor

// Build list of all member names for filtering
const allMemberNames = computed(() => {
  const names: string[] = [professor.name]
  members.researchers.forEach(m => names.push(m.name))
  members.phdStudents.forEach(m => names.push(m.name))
  members.msStudents.forEach(m => names.push(m.name))
  members.Intern.forEach(m => names.push(m.name))
  return names
})

// Check if any lab member is first author or corresponding author
const hasLabMemberAsFirstOrCorresponding = (pub: Publication): boolean => {
  const authors = pub.authors
  if (!authors || authors.length === 0) return false

  // Helper to check if Ho Won Lee is corresponding author
  const isHoWonLeeCorresponding = (): boolean => {
    for (const author of authors) {
      if (author && author.includes('*')) {
        const cleanName = author.replace(/[*+^]/g, '').trim().toLowerCase()
        if (cleanName.includes('ho') && cleanName.includes('won') && cleanName.includes('lee')) {
          return true
        }
      }
    }
    return false
  }

  // Check first author
  const firstAuthor = authors[0]
  if (firstAuthor) {
    const cleanFirst = firstAuthor.replace(/[*+^]/g, '').trim().toLowerCase()

    // Special case: Minh Tien Tran - only count if Ho Won Lee is corresponding
    if (cleanFirst.includes('minh') && cleanFirst.includes('tien') && cleanFirst.includes('tran')) {
      if (isHoWonLeeCorresponding()) {
        return true
      }
      // Don't return true for Minh Tien Tran without Ho Won Lee as corresponding
    } else {
      // Other lab members as first author
      for (const memberName of allMemberNames.value) {
        const nameParts = memberName.toLowerCase().split(' ')
        if (nameParts.every(part => cleanFirst.includes(part))) {
          return true
        }
      }
    }
  }

  // Check corresponding author (marked with *)
  for (const author of authors) {
    if (author && author.includes('*')) {
      const cleanName = author.replace(/[*+^]/g, '').trim().toLowerCase()
      for (const memberName of allMemberNames.value) {
        const nameParts = memberName.toLowerCase().split(' ')
        if (nameParts.every(part => cleanName.includes(part))) {
          return true
        }
      }
    }
  }

  return false
}

// Selected member filter (null = show all)
const selectedMember = ref<string | null>(null)

// Check if a publication has a specific member as author
const hasMember = (pub: Publication, memberName: string): boolean => {
  return pub.authors.some(a => {
    if (!a) return false
    const cleanName = a.replace(/[*+^]/g, '').trim().toLowerCase()
    // Check if the member name matches (partial match for flexibility)
    const nameParts = memberName.toLowerCase().split(' ')
    return nameParts.every(part => cleanName.includes(part))
  })
}

// Determine the role of a member in a publication
const getAuthorRole = (pub: Publication, memberName: string): 'corresponding' | 'first' | 'co-author' | null => {
  const authors = pub.authors
  const nameParts = memberName.toLowerCase().split(' ')

  for (let i = 0; i < authors.length; i++) {
    const author = authors[i]
    if (!author) continue
    const cleanName = author.replace(/[*+^]/g, '').trim().toLowerCase()

    if (nameParts.every(part => cleanName.includes(part))) {
      if (author.includes('*')) {
        return 'corresponding'
      }
      if (i === 0) {
        return 'first'
      }
      return 'co-author'
    }
  }
  return null
}

const getRoleBadge = (role: string | null): RoleBadge | null => {
  switch (role) {
    case 'corresponding':
      return { text: 'Corresponding', variant: 'soft-purple' }
    case 'first':
      return { text: 'First Author', variant: 'soft-green' }
    case 'co-author':
      return { text: 'Co-Author', variant: 'soft-gray' }
    default:
      return null
  }
}

const roleBadgeFor = (pub: Publication): RoleBadge | null =>
  selectedMember.value ? getRoleBadge(getAuthorRole(pub, selectedMember.value)) : null

const impactFactorFor = (pub: Publication): string | undefined =>
  pub.journal ? (IFData as Record<string, string>)[pub.journal] : undefined

const activeTab = ref<'journals' | 'conferences'>('journals')

const byIdDesc = (a: Publication, b: Publication) => {
  const idA = parseInt(a.id.replace(/[^0-9]/g, ''))
  const idB = parseInt(b.id.replace(/[^0-9]/g, ''))
  return idB - idA
}

// Filter journals by selected member
const filteredJournals = computed(() => {
  if (selectedMember.value) {
    return journals.value.filter(p => hasMember(p, selectedMember.value!))
  }
  return journals.value
})

// Filter conferences by selected member
const filteredConferences = computed(() => {
  if (selectedMember.value) {
    return conferences.value.filter(p => hasMember(p, selectedMember.value!))
  }
  return conferences.value
})

// Separate In Press / Accepted from filtered journals
const inPress = computed(() => {
  return filteredJournals.value
    .filter(p => p.status === 'In Press' || p.status === 'accepted')
    .sort(byIdDesc)
})

// Preprints / submitted from separate preprints.json
const inSubmission = computed(() => {
  const filtered = selectedMember.value
    ? preprints.value.filter(p => hasMember(p, selectedMember.value!))
    : preprints.value
  return filtered.sort(byIdDesc)
})

// Published journals grouped by year (newest first)
const publishedByYear = computed(() => {
  const published = filteredJournals.value.filter(p => !p.status)
  const years = [...new Set(published.map(p => p.year))].sort((a, b) => b - a)
  return years.map(year => ({
    year,
    publications: published.filter(p => p.year === year).sort(byIdDesc)
  }))
})

// Conferences grouped by year (newest first)
const conferencesByYear = computed(() => {
  const years = [...new Set(filteredConferences.value.map(p => p.year))].sort((a, b) => b - a)
  return years.map(year => ({
    year,
    publications: filteredConferences.value.filter(p => p.year === year).sort(byIdDesc)
  }))
})
</script>

<template>
  <div class="bg-gray-50 min-h-screen">
    <PageHero title="Publications" subtitle="Journal articles and conference presentations from AIMAP Lab.">
      <!-- Tabs -->
      <div class="flex flex-wrap mt-8 gap-4">
        <FilterPill :active="activeTab === 'journals'" @click="activeTab = 'journals'">
          Journals
        </FilterPill>
        <FilterPill :active="activeTab === 'conferences'" @click="activeTab = 'conferences'">
          Conferences
        </FilterPill>
      </div>

      <!-- Member Filter -->
      <div class="flex flex-wrap mt-4 gap-2">
        <FilterPill size="sm" :active="!selectedMember" @click="selectedMember = null">
          All
        </FilterPill>
        <FilterPill
          v-for="name in allMemberNames"
          :key="name"
          size="sm"
          :active="selectedMember === name"
          @click="selectedMember = name"
        >
          {{ name }}
        </FilterPill>
      </div>
    </PageHero>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Journals -->
      <div v-if="activeTab === 'journals'" class="space-y-8">
        <!-- In Submission Section -->
        <section v-if="inSubmission.length > 0">
          <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-3">
            <BaseBadge variant="solid-warning" size="md">In Submission</BaseBadge>
            {{ inSubmission.length }} papers
          </h2>
          <div class="space-y-4">
            <PublicationCard
              v-for="pub in inSubmission"
              :key="pub.id"
              :pub="pub"
              accent="submission"
              :impact-factor="impactFactorFor(pub)"
              :role-badge="roleBadgeFor(pub)"
            />
          </div>
        </section>

        <!-- In Press Section -->
        <section v-if="inPress.length > 0">
          <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-3">
            <BaseBadge variant="solid-accent" size="md">In Press</BaseBadge>
            {{ inPress.length }} papers
          </h2>
          <div class="space-y-4">
            <PublicationCard
              v-for="pub in inPress"
              :key="pub.id"
              :pub="pub"
              accent="inpress"
              :impact-factor="impactFactorFor(pub)"
              :role-badge="roleBadgeFor(pub)"
            />
          </div>
        </section>

        <!-- Published by Year -->
        <section v-for="yearGroup in publishedByYear" :key="yearGroup.year">
          <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-3">
            <BaseBadge variant="solid-gradient" size="md">{{ yearGroup.year }}</BaseBadge>
            {{ yearGroup.publications.length }} papers
          </h2>
          <div class="space-y-4">
            <PublicationCard
              v-for="pub in yearGroup.publications"
              :key="pub.id"
              :pub="pub"
              accent="published"
              :highlighted="hasLabMemberAsFirstOrCorresponding(pub)"
              :impact-factor="impactFactorFor(pub)"
              :role-badge="roleBadgeFor(pub)"
            />
          </div>
        </section>
      </div>

      <!-- Conferences -->
      <div v-if="activeTab === 'conferences'" class="space-y-8">
        <section v-for="yearGroup in conferencesByYear" :key="yearGroup.year">
          <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-3">
            <BaseBadge variant="solid-gradient" size="md">{{ yearGroup.year }}</BaseBadge>
            {{ yearGroup.publications.length }} papers
          </h2>
          <div class="space-y-4">
            <PublicationCard
              v-for="pub in yearGroup.publications"
              :key="pub.id"
              :pub="pub"
              kind="conference"
              :role-badge="roleBadgeFor(pub)"
            />
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
