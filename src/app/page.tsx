import Header from '@/components/Header'
import Sidebar from '@/components/Sidebar'
import JobList from '@/components/JobList'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      <main className="flex flex-1 gap-6 overflow-auto p-6">
        <Sidebar />
        <div className="flex-1 min-w-0">
          <div className="mx-auto max-w-4xl">
            <JobList />
          </div>
        </div>
      </main>
    </div>
  )
}
