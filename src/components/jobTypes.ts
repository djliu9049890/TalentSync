export type Job = {
  id: string
  title: string
  company: string
  location: string
  postedAt: string
  salary: string
  skills: string[]
  postedBy: {
    id: string
    name: string
    avatar: string
    url: string
  }
  postUrl: string
}

export type JobFilters = {
  employment: string[]
  experience: string[]
  recency: string[]
  locations: string[]
}
