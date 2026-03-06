import Header from '@/components/Header'
import Sidebar from '@/components/Sidebar'
import JobList from '@/components/JobList'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      <main className="flex flex-1 p-10">
        <div className="sticky top-24 self-start">
          <Sidebar />
        </div>
        <div className="flex-1 min-w-0">
          <div className="mx-auto pl-20 pr-10">
            <JobList />
          </div>
        </div>
      </main>
    </div>
  )
}
