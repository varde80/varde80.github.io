// Member types
export interface Education {
  degree: string
  field: string
  institution: string
  period: string
  thesis?: string
  advisor?: string
}

export interface Experience {
  period: string
  position: string
  Department?: string
  institution: string
}

export interface Professor {
  name: string
  title: string
  email: string
  phone?: string
  image: string
  bio?: string
  education: Education[]
  experience: Experience[]
  "Grants and Awards"?: string[]
  "Professional Activities/Memberships"?: string[]
}

export interface Member {
  id: string
  name: string
  position: string
  email: string
  image: string
  research?: string
  year?: number
}

export interface MembersData {
  researchers: Member[]
  phdStudents: Member[]
  msStudents: Member[]
  alumni: Member[]
}

// Research types
export interface ResearchArea {
  id: string
  title: string
  description: string
  image: string
  details: string[]
}

// Publication types
export interface Publication {
  id: string
  type?: 'journal' | 'conference'
  title: string
  authors: string[]
  journal?: string
  "Conference Name"?: string
  year: number
  volume?: string
  pages?: string
  doi?: string
  link?: string
  featured?: boolean
  impactFactor?: number | string
  highlightImage?: string
  status?: string
  "start date"?: string
  "end date"?: string
  Venue?: string
}

// Facility types
export interface Facility {
  id: string
  name: string
  description: string
  image: string
  specifications?: string[]
  manufacturer?: string
  model?: string
}

// Achievement types
export interface Patent {
  id: string
  title: string
  inventors: string[]
  patentNumber: string
  date: string
  country: string
}

export interface Award {
  id: string
  title: string
  recipient: string
  organization: string
  date: string
}

// Gallery types
export interface GalleryImage {
  id: string
  images: string[]
  title: string
  description?: string
  date?: string
  category?: string
}

// Software types
export interface Software {
  id: string
  name: string
  description: string
  github: string
  image?: string
  tags?: string[]
  year?: string
}

// Project types
export interface BilingualText {
  ko: string
  en: string
}

export interface Project {
  id: string
  title: BilingualText
  period: string | BilingualText
  role: BilingualText
  fundingAgency: string | BilingualText
  fundingAmount?: string | BilingualText
  status: 'ongoing' | 'completed'
}

// Contact types
export interface ContactInfo {
  address: string
  phone: string
  fax?: string
  email: string
  mapCoordinates?: {
    lat: number
    lng: number
  }
}
