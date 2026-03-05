export interface Recruiter {
  id: string
  name: string
  avatar: string
}

export interface Job {
  id: string
  title: string
  company: string
  location: string
  postedAt: string
  salary: string
  skills: string[]
  postedBy: Recruiter
}

// Placeholder avatars (initials); replace with real image URLs if desired
const avatar = (initials: string) =>
  `data:image/svg+xml,${encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="%236b7280"><circle cx="16" cy="16" r="16" fill="%23e5e7eb"/><text x="16" y="20" text-anchor="middle" font-size="12" font-family="system-ui,sans-serif" fill="%234b5563">${initials}</text></svg>`
  )}`

export const recruiters: Recruiter[] = [
  { id: '1', name: 'Sarah Jenkins', avatar: avatar('SJ') },
  { id: '2', name: 'Marcus Chen', avatar: avatar('MC') },
  { id: '3', name: 'Emily Rodriguez', avatar: avatar('ER') },
  { id: '4', name: 'David Kim', avatar: avatar('DK') },
]

export const jobs: Job[] = [
  {
    id: '1',
    title: 'Senior Frontend Engineer',
    company: 'Innovate AI',
    location: 'San Francisco, CA',
    postedAt: '2 days ago',
    salary: '$160k - $210k',
    skills: ['React', 'TypeScript', 'Tailwind'],
    postedBy: recruiters[0],
  },
  {
    id: '2',
    title: 'Product Designer',
    company: 'Creative Studio',
    location: 'Remote',
    postedAt: '1 week ago',
    salary: '$120k - $155k',
    skills: ['Figma', 'UX Research', 'Prototyping'],
    postedBy: recruiters[1],
  },
  {
    id: '3',
    title: 'Full Stack Developer',
    company: 'TechFlow',
    location: 'New York, NY',
    postedAt: '3 days ago',
    salary: '$140k - $180k',
    skills: ['Node.js', 'React', 'PostgreSQL'],
    postedBy: recruiters[2],
  },
  {
    id: '4',
    title: 'DevOps Engineer',
    company: 'CloudScale',
    location: 'Austin, TX',
    postedAt: '5 days ago',
    salary: '$150k - $190k',
    skills: ['Kubernetes', 'AWS', 'Terraform'],
    postedBy: recruiters[3],
  },
  {
    id: '5',
    title: 'Data Scientist',
    company: 'DataDrive',
    location: 'Boston, MA',
    postedAt: '1 day ago',
    salary: '$130k - $170k',
    skills: ['Python', 'ML', 'SQL'],
    postedBy: recruiters[0],
  },
  {
    id: '6',
    title: 'UX Writer',
    company: 'Product Co',
    location: 'Remote',
    postedAt: '4 days ago',
    salary: '$95k - $125k',
    skills: ['Copywriting', 'Content Strategy', 'Research'],
    postedBy: recruiters[1],
  },
]

export const employmentTypes = ['Full-time', 'Contract', 'Remote', 'Part-time', 'Freelance'] as const
export const experienceLevels = ['Entry', 'Mid-level', 'Senior', 'Lead', 'Executive'] as const
