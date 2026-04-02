'use client'

import { Briefcase, Search } from 'lucide-react'

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-screen-2xl items-center justify-between gap-4 px-4 py-6 sm:px-6 lg:px-10">
        <div className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-[#0CCB7A] to-[#08A265] text-white">
            <Briefcase className="h-5 w-5" />
          </div>
          <span className="text-xl font-semibold tracking-tight">TalentSync</span>
        </div>

        <div className="relative flex-1 max-w-2xl">
          <Search className="absolute left-5 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
          <input
            type="search"
            placeholder="Search by title, company, or skills..."
            className="font-[490] w-full rounded-lg border border-gray-200 bg-gray-50 py-4 pl-[51px] pr-4 text-sm placeholder:text-gray-500 focus:border-gray-300 focus:bg-white focus:outline-none focus:ring-1 focus:ring-gray-300"
          />
        </div>

        <div className="flex items-center gap-6">
          {/* <a
            href="#"
            className="text-sm font-semibold text-gray-600 hover:text-gray-900"
          >
            Log In
          </a> */} {/* Implement login later */}
          <button className="flex gap-2 rounded-lg bg-[#08A265] px-6 py-3 text-sm font-medium text-white hover:bg-gray-800 transition-colors">
            <span className="text-[20px] mt-[0.5px] font-thin">+</span>
            <span className="text-[14px] font-medium">Post a Job</span>
          </button>
        </div>
      </div>
    </header>
  )
}
