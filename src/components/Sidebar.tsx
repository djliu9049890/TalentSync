'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Filter, Bell } from 'lucide-react'
import { recruiters, employmentTypes, experienceLevels } from '@/data/mockJobs'

export default function Sidebar() {
  const [employment, setEmployment] = useState<Set<string>>(new Set())
  const [experience, setExperience] = useState<Set<string>>(new Set())
  const [selectedRecruiters, setSelectedRecruiters] = useState<Set<string>>(new Set())

  const toggle = (
    set: React.Dispatch<React.SetStateAction<Set<string>>>,
    value: string
  ) => {
    set((prev) => {
      const next = new Set(prev)
      if (next.has(value)) next.delete(value)
      else next.add(value)
      return next
    })
  }

  const clearAll = () => {
    setEmployment(new Set())
    setExperience(new Set())
    setSelectedRecruiters(new Set())
  }

  const hasFilters = employment.size > 0 || experience.size > 0 || selectedRecruiters.size > 0

  return (
    <aside className="flex w-72 shrink-0 flex-col gap-4">
      {/* Filters box */}
      <div className="rounded-xl bg-white p-6 shadow-sm">
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-gray-500" />
            <h2 className="font-semibold text-gray-900">Filters</h2>
          </div>
          {hasFilters && (
            <button
              onClick={clearAll}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Clear all
            </button>
          )}
        </div>

        <section className="mb-6">
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-gray-500">
            Employment Type
          </h3>
          <ul className="space-y-2">
            {employmentTypes.map((type) => (
              <li key={type} className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id={`emp-${type}`}
                  checked={employment.has(type)}
                  onChange={() => toggle(setEmployment, type)}
                  className="checkbox-custom"
                />
                <label htmlFor={`emp-${type}`} className="text-sm text-gray-700">
                  {type}
                </label>
              </li>
            ))}
          </ul>
        </section>

        <section className="mb-6">
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-gray-500">
            Experience Level
          </h3>
          <ul className="space-y-2">
            {experienceLevels.map((level) => (
              <li key={level} className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id={`exp-${level}`}
                  checked={experience.has(level)}
                  onChange={() => toggle(setExperience, level)}
                  className="checkbox-custom"
                />
                <label htmlFor={`exp-${level}`} className="text-sm text-gray-700">
                  {level}
                </label>
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-gray-500">
            Trusted Recruiters
          </h3>
          <ul className="space-y-3">
            {recruiters.map((r) => (
              <li key={r.id} className="flex items-center gap-4">
                <input
                  type="checkbox"
                  id={`recruiter-${r.id}`}
                  checked={selectedRecruiters.has(r.id)}
                  onChange={() => toggle(setSelectedRecruiters, r.id)}
                  className="checkbox-custom"
                />
                <div className="flex min-w-0 flex-1 items-center gap-2">
                  <Image
                    src={r.avatar}
                    alt={r.name}
                    width={32}
                    height={32}
                    className="h-6 w-6 shrink-0 rounded-full object-cover bg-gray-200"
                    unoptimized
                  />
                  <label htmlFor={`recruiter-${r.id}`} className="cursor-pointer text-sm text-gray-700">
                    {r.name}
                  </label>
                </div>
              </li>
            ))}
          </ul>
        </section>
      </div>

      {/* Alerts box */}
      <div className="rounded-xl bg-gray-800 p-4 text-white shadow-sm">
        <div className="mb-2 flex items-center gap-2">
          <Bell className="h-4 w-4" />
          <span className="font-medium">Get personalized alerts</span>
        </div>
        <p className="mb-4 text-sm text-gray-300">
          We&apos;ll notify you as soon as a matching job is posted.
        </p>
        <button className="w-full rounded-lg bg-gray-700 py-2.5 text-sm font-medium text-white hover:bg-gray-600 transition-colors">
          Enable Notifications
        </button>
      </div>
    </aside>
  )
}
