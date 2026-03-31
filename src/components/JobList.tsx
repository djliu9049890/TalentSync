'use client'

import { useState } from 'react'
import { Sparkles } from 'lucide-react'
import JobCard from './JobCard'
import { jobs } from '@/data/mockJobs'

export default function JobList() {
  const [tab, setTab] = useState<'latest' | 'popular'>('latest')

  return (
    <div className="min-w-0 flex-1">
      <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-col gap-[10px]">
          <h1 className="flex items-start gap-2 text-2xl font-semibold text-gray-900">
            <span>Recommended for you</span>
            <Sparkles className="mt-0.5 h-5 w-5 text-[#08A265]" />
          </h1>
          <p className="text-sm font-medium text-gray-500">Showing {jobs.length} open positions</p>
        </div>
        <div className="flex rounded-full border border-gray-200 bg-white p-1">
          <button
            onClick={() => setTab('latest')}
            className={`rounded-full px-5 py-2 text-sm transition-colors ${
              tab === 'latest'
                ? 'bg-gray-100 font-semibold text-gray-900'
                : 'font-normal text-gray-500 hover:text-gray-700'
            }`}
          >
            Latest
          </button>
          <button
            onClick={() => setTab('popular')}
            className={`rounded-full px-5 py-2 text-sm transition-colors ${
              tab === 'popular'
                ? 'bg-gray-100 font-semibold text-gray-900'
                : 'font-normal text-gray-500 hover:text-gray-700'
            }`}
          >
            Popular
          </button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        {jobs.map((job) => (
          <div
            key={job.id}
            className="group rounded-xl bg-white p-4 shadow-sm transition-all ease-in-out duration-1000 hover:-translate-y-1 hover:shadow-lg hover:ring-1 hover:ring-gray-300 sm:p-7"
          >
            <JobCard job={job} />
          </div>
        ))}
      </div>
    </div>
  )
}
