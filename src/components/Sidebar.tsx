'use client'

import { useMemo, useState } from 'react'
import {
  BriefcaseBusiness,
  ChartNoAxesColumnIncreasing,
  Check,
  Clock3,
  ClockArrowUp,
  FileText,
  Filter,
  Flag,
  Globe,
  MapPin,
  Monitor,
  Search,
  Star,
  Trophy,
  Workflow,
  X,
} from 'lucide-react'
import type { Dispatch, SetStateAction } from 'react'
import type { JobFilters } from '@/components/jobTypes'
import { employmentTypes, experienceLevels, locationOptions, recencyOptions } from '@/data/mockJobs'

const employmentIcons: Record<(typeof employmentTypes)[number], typeof BriefcaseBusiness> = {
  'Full-time': BriefcaseBusiness,
  Contract: FileText,
  Remote: Monitor,
  'Part-time': Clock3
}

const experienceIcons: Record<(typeof experienceLevels)[number], typeof BriefcaseBusiness> = {
  Entry: Workflow,
  'Mid-level': ChartNoAxesColumnIncreasing,
  Senior: Star,
  Lead: Flag,
  Executive: Trophy,
}

const recencyIcons: Record<(typeof recencyOptions)[number], typeof BriefcaseBusiness> = {
  '1 day': ClockArrowUp,
  '1 week': ClockArrowUp,
  '1 month': ClockArrowUp,
}

interface FilterOptionProps {
  checked: boolean
  icon: typeof BriefcaseBusiness
  id: string
  label: string
  onChange: () => void
  type?: 'checkbox' | 'radio'
}

function FilterOption({
  checked,
  icon: Icon,
  id,
  label,
  onChange,
  type = 'checkbox',
}: FilterOptionProps) {
  return (
    <li>
      <input
        type={type}
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

interface SidebarProps {
  filters: JobFilters
  onFiltersChange: Dispatch<SetStateAction<JobFilters>>
}

export default function Sidebar({ filters, onFiltersChange }: SidebarProps) {
  const [locationQuery, setLocationQuery] = useState('')
  const [isLocationFocused, setIsLocationFocused] = useState(false)

  const employment = new Set(filters.employment)
  const experience = new Set(filters.experience)
  const recency = new Set(filters.recency)
  const locations = new Set(filters.locations)

  const toggle = (key: keyof JobFilters, value: string) => {
    onFiltersChange((prev) => {
      const nextValues = new Set(prev[key])
      if (nextValues.has(value)) {
        nextValues.delete(value)
      } else {
        nextValues.add(value)
      }

      return {
        ...prev,
        [key]: Array.from(nextValues),
      }
    })
  }

  const toggleRecency = (value: string) => {
    onFiltersChange((prev) => ({
      ...prev,
      recency: prev.recency[0] === value ? [] : [value],
    }))
  }

  const clearAll = () => {
    onFiltersChange({
      employment: [],
      experience: [],
      recency: [],
      locations: [],
    })
    setLocationQuery('')
  }

  const hasFilters =
    employment.size > 0 || experience.size > 0 || recency.size > 0 || locations.size > 0

  const filteredLocations = useMemo(() => {
    const query = locationQuery.trim().toLowerCase()
    if (!query) return locationOptions
    return locationOptions.filter((location) => location.toLowerCase().includes(query))
  }, [locationQuery])

  const shouldShowLocationResults = isLocationFocused && filteredLocations.length > 0

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
                onChange={() => toggle('employment', type)}
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
                onChange={() => toggle('experience', level)}
                icon={experienceIcons[level]}
                label={level}
              />
            ))}
          </ul>
        </section>

        <section className="mb-8">
          <h3 className="mb-4 text-[15px] font-semibold text-[#2d3446]">Location</h3>
          <div className="relative">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#9aa3b2]" />
              <input
                type="text"
                value={locationQuery}
                onChange={(event) => setLocationQuery(event.target.value)}
                onFocus={() => setIsLocationFocused(true)}
                onBlur={() => {
                  window.setTimeout(() => setIsLocationFocused(false), 120)
                }}
                placeholder="Search locations"
                className="w-full rounded-xl border border-[#e6e9ef] bg-white py-3 pl-9 pr-3 text-sm text-[#2d3446] placeholder:text-[#9aa3b2] transition focus:border-[#b8d0fa] focus:outline-none focus:ring-2 focus:ring-[#dfeafe]"
              />
            </div>

            {shouldShowLocationResults && (
              <ul className="absolute left-0 right-0 top-[calc(100%+8px)] z-20 max-h-56 space-y-2 overflow-y-auto rounded-xl border border-[#e6e9ef] bg-white p-2 shadow-[0_10px_30px_rgba(15,23,42,0.08)]">
                {filteredLocations.map((location) => (
                  <li key={location}>
                    <button
                      type="button"
                      onMouseDown={(event) => event.preventDefault()}
                      onClick={() => {
                        toggle('locations', location)
                        setLocationQuery('')
                        setIsLocationFocused(true)
                      }}
                      className={`flex w-full items-center justify-between rounded-lg px-3 py-2.5 text-left transition ${
                        locations.has(location)
                          ? 'bg-[#f1f6ff] text-[#6f98df]'
                          : 'text-[#5f6678] hover:bg-[#f8faff]'
                      }`}
                    >
                      <span className="flex items-center gap-3">
                        <MapPin className="h-4 w-4" />
                        <span className="text-sm font-medium">{location}</span>
                      </span>
                      {locations.has(location) && (
                        <span className="flex h-5 w-5 items-center justify-center rounded-full bg-[#86a8e6]">
                          <Check className="h-3 w-3 text-[#f6f9ff]" strokeWidth={3} />
                        </span>
                      )}
                    </button>
                  </li>
                ))}
              </ul>
            )}

            {isLocationFocused && filteredLocations.length === 0 && locationQuery.trim() && (
              <div className="absolute left-0 right-0 top-[calc(100%+8px)] z-20 rounded-xl border border-[#e6e9ef] bg-white px-4 py-3 text-sm text-[#7e8699] shadow-[0_10px_30px_rgba(15,23,42,0.08)]">
                No matching locations
              </div>
            )}
          </div>

          {locations.size > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {Array.from(locations).map((location) => (
                <button
                  key={location}
                  type="button"
                  onClick={() => toggle('locations', location)}
                  className="inline-flex items-center gap-1 rounded-full bg-[#eef3ff] px-3 py-1.5 text-xs font-medium text-[#5e86d2] transition hover:bg-[#e2ebff]"
                >
                  <span>{location}</span>
                  <X className="h-3 w-3" />
                </button>
              ))}
            </div>
          )}
        </section>

        <section>
          <h3 className="mb-4 text-[15px] font-semibold text-[#2d3446]">Date Posted</h3>
          <ul className="space-y-3">
            {recencyOptions.map((option) => (
              <FilterOption
                key={option}
                id={`recency-${option}`}
                checked={recency.has(option)}
                onChange={() => toggleRecency(option)}
                icon={recencyIcons[option]}
                label={option}
                type="radio"
              />
            ))}
          </ul>
        </section>
      </div>
    </aside>
  )
}
