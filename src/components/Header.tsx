'use client'

import { Briefcase, Search } from 'lucide-react'

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-screen-2xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-10">
        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gray-900 text-white">
            <Briefcase className="h-5 w-5" />
          </div>
          <span className="text-xl font-semibold tracking-tight">TalentSync</span>
        </div>

        <div className="relative flex-1 max-w-2xl">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <input
            type="search"
            placeholder="Search by title, company, or skills..."
            className="w-full rounded-lg border border-gray-200 bg-gray-50 py-2.5 pl-10 pr-4 text-sm placeholder:text-gray-500 focus:border-gray-300 focus:bg-white focus:outline-none focus:ring-1 focus:ring-gray-300"
          />
        </div>

        <div className="flex items-center gap-4">
          <a
            href="#"
            className="text-sm font-medium text-gray-700 hover:text-gray-900"
          >
            Log In
          </a>
          <button className="rounded-lg bg-gray-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-gray-800 transition-colors">
            Post a Job
          </button>
        </div>
      </div>
    </header>
  )
}
