'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'
import {
  BriefcaseBusiness,
  ChartNoAxesColumnIncreasing,
  Check,
  Clock3,
  FileText,
  Filter,
  Flag,
  Globe,
  Monitor,
  Star,
  Trophy,
  Workflow,
} from 'lucide-react'
import { recruiters, employmentTypes, experienceLevels } from '@/data/mockJobs'

const employmentIcons: Record<(typeof employmentTypes)[number], typeof BriefcaseBusiness> = {
  'Full-time': BriefcaseBusiness,
  Contract: FileText,
  Remote: Monitor,
  'Part-time': Clock3,
  Freelance: Globe,
}

const experienceIcons: Record<(typeof experienceLevels)[number], typeof BriefcaseBusiness> = {
  Entry: Workflow,
  'Mid-level': ChartNoAxesColumnIncreasing,
  Senior: Star,
  Lead: Flag,
  Executive: Trophy,
}

interface FilterOptionProps {
  checked: boolean
  icon: typeof BriefcaseBusiness
  id: string
  label: string
  onChange: () => void
}

function FilterOption({ checked, icon: Icon, id, label, onChange }: FilterOptionProps) {
  return (
    <li>
      <input
        type="checkbox"
        id={id}
        checked={checked}
        onChange={onChange}
        className="sr-only"
      />
      <label
        htmlFor={id}
        className={`flex cursor-pointer items-center justify-between rounded-xl border px-4 py-4 transition-colors ${
          checked
            ? 'border-[#b8d0fa] bg-[#f1f6ff]'
            : 'border-[#e6e9ef] bg-white hover:border-[#c6cfda]'
        }`}
      >
        <span className="flex items-center gap-3">
          <Icon className={`h-4 w-4 ${checked ? 'text-[#6f98df]' : 'text-[#7e8699]'}`} />
          <span className={`text-sm font-medium ${checked ? 'text-[#6f98df]' : 'text-[#5f6678]'}`}>
            {label}
          </span>
        </span>
        {checked && (
          <span className="flex h-5 w-5 items-center justify-center rounded-full bg-[#86a8e6]">
            <Check className="h-3 w-3 text-[#f6f9ff]" strokeWidth={3} />
          </span>
        )}
      </label>
    </li>
  )
}

export default function Sidebar() {
  const [employment, setEmployment] = useState<Set<string>>(new Set())
  const [experience, setExperience] = useState<Set<string>>(new Set())
  const [selectedRecruiters, setSelectedRecruiters] = useState<Set<string>>(new Set())

  useEffect(() => {
    const savedEmployment = window.localStorage.getItem('sidebar-employment')
    const savedExperience = window.localStorage.getItem('sidebar-experience')
    const savedRecruiters = window.localStorage.getItem('sidebar-recruiters')

    if (savedEmployment) {
      setEmployment(new Set(JSON.parse(savedEmployment)))
    }
    if (savedExperience) {
      setExperience(new Set(JSON.parse(savedExperience)))
    }
    if (savedRecruiters) {
      setSelectedRecruiters(new Set(JSON.parse(savedRecruiters)))
    }
  }, [])

  useEffect(() => {
    window.localStorage.setItem('sidebar-employment', JSON.stringify(Array.from(employment)))
  }, [employment])

  useEffect(() => {
    window.localStorage.setItem('sidebar-experience', JSON.stringify(Array.from(experience)))
  }, [experience])

  useEffect(() => {
    window.localStorage.setItem('sidebar-recruiters', JSON.stringify(Array.from(selectedRecruiters)))
  }, [selectedRecruiters])

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
      <div className="rounded-[22px] border border-[#e8edf2] bg-white p-7 shadow-[0_8px_30px_rgba(15,23,42,0.04)]">
        <div className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Filter className="h-4 w-4 text-[#08A265]" />
            <h2 className="text-[18px] font-semibold text-[#252b3b]">Filters</h2>
          </div>
          <button
            onClick={clearAll}
            disabled={!hasFilters}
            className={`text-sm font-medium transition ${
              hasFilters
                ? 'text-[#34c47f] hover:text-[#08A265]'
                : 'cursor-default text-[#b8c0cc]'
            }`}
          >
            Clear all
          </button>
        </div>

        <section className="mb-8">
          <h3 className="mb-4 text-[15px] font-semibold text-[#2d3446]">Employment Type</h3>
          <ul className="space-y-3">
            {employmentTypes.map((type) => (
              <FilterOption
                key={type}
                id={`emp-${type}`}
                checked={employment.has(type)}
                onChange={() => toggle(setEmployment, type)}
                icon={employmentIcons[type]}
                label={type}
              />
            ))}
          </ul>
        </section>

        <section className="mb-8">
          <h3 className="mb-4 text-[15px] font-semibold text-[#2d3446]">Experience Level</h3>
          <ul className="space-y-3">
            {experienceLevels.map((level) => (
              <FilterOption
                key={level}
                id={`exp-${level}`}
                checked={experience.has(level)}
                onChange={() => toggle(setExperience, level)}
                icon={experienceIcons[level]}
                label={level}
              />
            ))}
          </ul>
        </section>

        <section>
          <h3 className="mb-4 text-[15px] font-semibold text-[#2d3446]">Trusted Recruiters</h3>
          <ul className="space-y-3">
            {recruiters.map((r) => {
              const checked = selectedRecruiters.has(r.id)

              return (
                <li key={r.id}>
                  <input
                    type="checkbox"
                    id={`recruiter-${r.id}`}
                    checked={checked}
                    onChange={() => toggle(setSelectedRecruiters, r.id)}
                    className="sr-only"
                  />
                  <label
                    htmlFor={`recruiter-${r.id}`}
                    className={`flex cursor-pointer items-center justify-between rounded-xl border px-4 py-3 transition-colors ${
                      checked
                        ? 'border-[#b8d0fa] bg-[#f1f6ff]'
                        : 'border-[#e6e9ef] bg-white hover:border-[#c6cfda]'
                    }`}
                  >
                    <span className="flex min-w-0 items-center gap-3">
                      <Image
                        src={r.avatar}
                        alt={r.name}
                        width={28}
                        height={28}
                        className="h-7 w-7 shrink-0 rounded-full object-cover bg-[#eef1f5]"
                        unoptimized
                      />
                      <span className={`truncate text-sm font-medium ${checked ? 'text-[#6f98df]' : 'text-[#5f6678]'}`}>
                        {r.name}
                      </span>
                    </span>
                    {checked ? (
                      <span className="flex h-5 w-5 items-center justify-center rounded-full bg-[#86a8e6]">
                        <Check className="h-3 w-3 text-[#f6f9ff]" strokeWidth={3} />
                      </span>
                    ) : (
                      <span className="h-5 w-5" />
                    )}
                  </label>
                </li>
              )
            })}
          </ul>
        </section>
      </div>
    </aside>
  )
}
