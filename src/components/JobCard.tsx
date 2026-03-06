'use client'

import Image from 'next/image'
import { Briefcase, MapPin, Clock, CheckCircle, ChevronRight } from 'lucide-react'
import type { Job } from '@/data/mockJobs'

interface JobCardProps {
  job: Job
}

export default function JobCard({ job }: JobCardProps) {
  return (
    <article className="group flex gap-4">
      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-gray-100 text-gray-500 group-hover:text-gray-800">
        <Briefcase className="h-6 w-6" />
      </div>

      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="font-semibold text-gray-900">{job.title}</h3>
            <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-gray-500">
              <span className="flex items-center gap-1">
                <CheckCircle className="h-4 w-4 text-emerald-500" />
                {job.company}
              </span>
              <span className="flex items-center gap-1">
                <MapPin className="h-4 w-4" />
                {job.location}
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                {job.postedAt}
              </span>
            </div>
          </div>
          <div className="shrink-0 font-semibold text-gray-900">{job.salary}</div>
        </div>

        <div className="mt-3 flex flex-wrap gap-2">
          {job.skills.map((skill) => (
            <span
              key={skill}
              className="rounded-md bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700"
            >
              {skill}
            </span>
          ))}
        </div>

        <div className="mt-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Image
              src={job.postedBy.avatar}
              alt={job.postedBy.name}
              width={24}
              height={24}
              className="h-6 w-6 rounded-full object-cover bg-gray-200"
              unoptimized
            />
            <span className="text-sm text-gray-500">
              Posted by {job.postedBy.name}
            </span>
          </div>
          <a
            href="#"
            className="inline-flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-gray-900 group-hover:underline"
          >
            Details
            <ChevronRight className="h-4 w-4" />
          </a>
        </div>
      </div>
    </article>
  )
}
