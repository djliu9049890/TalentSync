'use client'

import { Briefcase, MapPin, Clock, Check, ChevronRight } from 'lucide-react'
import type { Job } from './JobList'

interface JobCardProps {
  job: Job
}

function formatPostedTime(postedAt: string) {
  const postedDate = new Date(postedAt)

  if (Number.isNaN(postedDate.getTime())) {
    return postedAt
  }

  const diffMs = Date.now() - postedDate.getTime()
  const diffDays = Math.max(1, Math.ceil(diffMs / (1000 * 60 * 60 * 24)))

  if (diffDays < 7) {
    return `${diffDays} day${diffDays === 1 ? '' : 's'} ago`
  }

  if (diffDays < 30) {
    const diffWeeks = Math.ceil(diffDays / 7)
    return `${diffWeeks} week${diffWeeks === 1 ? '' : 's'} ago`
  }

  const diffMonths = Math.ceil(diffDays / 30)
  return `${diffMonths} month${diffMonths === 1 ? '' : 's'} ago`
}

export default function JobCard({ job }: JobCardProps) {
  const postedTimeLabel = formatPostedTime(job.postedAt)

  return (
    <article className="group flex gap-6">
      <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-lg bg-gray-100 text-gray-500 transition-colors group-hover:text-gray-800">
        <Briefcase className="h-6 w-6" />
      </div>

      <div className="min-w-0 flex-1 flex flex-col gap-[2px]">
        <div className="flex items-start justify-between gap-4">
          <h3 className="font-semibold text-gray-900 max-w-[500px]">{job.title}</h3>
          <div className="shrink-0 font-semibold text-gray-900">{job.salary}</div>
        </div>
        <div className="flex items-start justify-between gap-4">
            <div className="mt-1 flex flex-wrap items-center gap-x-5 gap-y-1 text-sm text-gray-500">
              <span className="flex items-center gap-1 font-semibold">
                <span className="flex h-4 w-4 items-center justify-center rounded-full bg-emerald-500">
                  <Check className="h-3 w-3 text-white" strokeWidth={3} />
                </span>
                {job.company}
              </span>
              <span className="flex min-w-0 max-w-[250px] items-center gap-1 font-[450]">
                <MapPin className="h-4 w-4 shrink-0" />
                <span className="truncate whitespace-nowrap">{job.location}</span>
              </span>
              <span className="flex items-center gap-1 font-[450]">
                <Clock className="h-4 w-4" />
                {postedTimeLabel}
              </span>
            </div>
        </div>

        <div className="mt-3 flex flex-wrap gap-2 max-w-[500px]">
          {job.skills.map((skill) => (
            <span
              key={skill}
              className="rounded-md bg-[#E3F7ED] px-3 py-1.5 text-xs font-[550] text-emerald-500"
            >
              {skill}
            </span>
          ))}
        </div>

        <div className="mt-1 flex items-center justify-between">
          <a
            href={job.postedBy.url}
            className="flex items-center gap-2 rounded-lg px-2 py-1.5 transition-colors hover:bg-gray-50"
          >
            <img
              src={job.postedBy.avatar}
              alt={job.postedBy.name}
              className="h-6 w-6 rounded-full object-cover bg-gray-200"
            />
            <span className="text-sm text-gray-500 font-[450]">
              Posted by {job.postedBy.name}
            </span>
          </a>
          <a
            href={job.postUrl}
            className="inline-flex items-center gap-2 rounded-xl border border-gray-200 bg-white px-5 py-3 text-sm font-medium text-gray-700 transition-colors hover:border-gray-400 hover:text-gray-900"
          >
            View Details
            <ChevronRight className="h-4 w-4 text-[#08A265]" />
          </a>
        </div>
      </div>
    </article>
  )
}
