// Member types
export interface Professor {
  name: string
  title: string
  email: string
  phone?: string
  image: string
  bio: string
  education: string[]
  experience: string[]
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
  professor: Professor
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
  journal: string
  year: number
  volume?: string
  pages?: string
  doi?: string
  link?: string
  featured?: boolean
  impactFactor?: number | string
  highlightImage?: string
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
