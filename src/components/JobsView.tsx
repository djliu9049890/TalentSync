'use client'

import { useEffect, useState } from 'react'
import Sidebar from '@/components/Sidebar'
import JobList from '@/components/JobList'
import type { Job, JobFilters } from '@/components/jobTypes'
import { defaultAvatar } from '@/data/mockJobs'
import { supabase } from '@/lib/supabase'

type SupabasePostRow = {
  id: number
  job_title: string | null
  company: string | null
  location: string | null
  salary: string | null
  skills: string[] | null
  posted_at: string
  hiring_contact_name: string | null
  hiring_contact_linkedin_url: string | null
  recruiter_id: number
  linkedin_post_url: string | null
}

const defaultFilters: JobFilters = {
  employment: [],
  experience: [],
  recency: [],
  locations: [],
}

function mapPostsToJobs(posts: SupabasePostRow[]) {
  return posts.map((post) => ({
    id: String(post.id),
    title: post.job_title ?? 'Untitled Role',
    company: post.company ?? 'Unknown Company',
    location: post.location ?? 'Unknown Location',
    postedAt: post.posted_at,
    salary: post.salary ?? 'Salary not listed',
    skills: post.skills ?? [],
    postedBy: {
      id: String(post.recruiter_id),
      name: post.hiring_contact_name ?? 'Unknown Recruiter',
      avatar: defaultAvatar(),
      url: post.hiring_contact_linkedin_url ?? '#',
    },
    postUrl: post.linkedin_post_url ?? '#',
  }))
}

export default function JobsView() {
  const [filters, setFilters] = useState<JobFilters>(defaultFilters)
  const [jobs, setJobs] = useState<Job[]>([])
  const [hasLoadedFilters, setHasLoadedFilters] = useState(false)

  useEffect(() => {
    const savedEmployment = window.localStorage.getItem('sidebar-employment')
    const savedExperience = window.localStorage.getItem('sidebar-experience')
    const savedRecency = window.localStorage.getItem('sidebar-recency')
    const savedLocations = window.localStorage.getItem('sidebar-locations')

    setFilters({
      employment: savedEmployment ? JSON.parse(savedEmployment) : [],
      experience: savedExperience ? JSON.parse(savedExperience) : [],
      recency: savedRecency ? JSON.parse(savedRecency) : [],
      locations: savedLocations ? JSON.parse(savedLocations) : [],
    })
    setHasLoadedFilters(true)
  }, [])

  useEffect(() => {
    if (!hasLoadedFilters) {
      return
    }

    window.localStorage.setItem('sidebar-employment', JSON.stringify(filters.employment))
    window.localStorage.setItem('sidebar-experience', JSON.stringify(filters.experience))
    window.localStorage.setItem('sidebar-recency', JSON.stringify(filters.recency))
    window.localStorage.setItem('sidebar-locations', JSON.stringify(filters.locations))
  }, [filters, hasLoadedFilters])

  useEffect(() => {
    if (!hasLoadedFilters) {
      return
    }

    async function loadJobs() {
      let query = supabase
        .from('posts')
        .select(`
          id,
          job_title,
          company,
          location,
          salary,
          skills,
          posted_at,
          hiring_contact_name,
          hiring_contact_linkedin_url,
          recruiter_id,
          linkedin_post_url
        `)
        .order('posted_at', { ascending: false })

      if (filters.employment.length > 0) {
        query = query.in('employment_type', filters.employment)
      }

      if (filters.experience.length > 0) {
        query = query.in('experience_level', filters.experience)
      }

      const recencyOption = filters.recency[0]
      if (recencyOption) {
        const daysByOption: Record<string, number> = {
          '1 day': 1,
          '1 week': 7,
          '1 month': 30,
        }
        const days = daysByOption[recencyOption]

        if (typeof days === 'number') {
          const threshold = new Date()
          threshold.setDate(threshold.getDate() - days)
          query = query.gte('posted_at', threshold.toISOString())
        }
      }

      if (filters.locations.length > 0) {
        const locationClauses = filters.locations.map(
          (location) => {
            const safeLocation = location.replace(/[%()]/g, '').replace(/"/g, '\\"')
            return `location.ilike."%${safeLocation}%"`
          }
        )
        query = query.or(locationClauses.join(','))
      }

      const { data, error } = await query

      if (error) {
        console.error('Supabase error:', error)
        setJobs([])
        return
      }

      setJobs(mapPostsToJobs((data ?? []) as SupabasePostRow[]))
    }

    loadJobs()
  }, [filters, hasLoadedFilters])

  return (
    <>
      <div className="relative sticky top-0 self-start">
        <Sidebar filters={filters} onFiltersChange={setFilters} />
      </div>
      <div className="relative flex-1 min-w-0">
        <div className="mx-auto pl-20 pr-10">
          <JobList jobs={jobs} />
        </div>
      </div>
    </>
  )
}
