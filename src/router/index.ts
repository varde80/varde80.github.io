import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../pages/HomePage.vue')
  },
  {
    path: '/members',
    name: 'Members',
    component: () => import('../pages/MembersPage.vue')
  },
  {
    path: '/research',
    name: 'Research',
    component: () => import('../pages/ResearchPage.vue')
  },
  {
    path: '/facilities',
    name: 'Facilities',
    component: () => import('../pages/FacilitiesPage.vue')
  },
  {
    path: '/achievements',
    name: 'Achievements',
    component: () => import('../pages/AchievementsPage.vue')
  },
  {
    path: '/gallery',
    name: 'Gallery',
    component: () => import('../pages/GalleryPage.vue')
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../pages/ContactPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
