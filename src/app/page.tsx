import Header from '@/components/Header'
import Sidebar from '@/components/Sidebar'
import JobList from '@/components/JobList'
import { Job } from '@/components/JobList'
import { supabase } from '@/lib/supabase'
import { defaultAvatar } from '@/data/mockJobs'

export default async function Home() {
  const { data, error } = await supabase
    .from('posts')
    .select(`
      id,
      job_title,
      company,
      location,
      salary,
      skills,
      posted_at,
      hiring_contact_name,
      hiring_contact_linkedin_url,
      recruiter_id,
      linkedin_post_url
    `).order('posted_at', { ascending: false })

  if (error) {
    console.error('Supabase error: ', error)
  }

  const jobs: Job[] = (data ?? []).map( (post) => ({
    id: String(post.id),
    title: post.job_title ?? 'Untitled Role',
    company: post.company ?? 'Unknown Company',
    location: post.location ?? 'Unknown Location',
    postedAt: post.posted_at,
    salary: post.salary ?? 'Salary not listed',
    skills: post.skills ?? [],
    postedBy: {
      id: post.recruiter_id,
      name: post.hiring_contact_name,
      url: post.hiring_contact_linkedin_url,
      avatar: defaultAvatar()
    },
    postUrl: post.linkedin_post_url
  }))

  return (
    <div className="min-h-screen flex flex-col bg-[#f8faf8]">
      <Header />
      <main className="relative flex flex-1 p-10">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(214,245,220,0.68),_transparent_22%),linear-gradient(120deg,_rgba(240,248,241,0.82)_0%,_rgba(248,249,246,0.9)_28%,_rgba(221,235,255,0.7)_70%,_rgba(248,250,255,0.96)_100%)]" />
        <div className="relative sticky top-0 self-start">
          <Sidebar />
        </div>
        <div className="relative flex-1 min-w-0">
          <div className="mx-auto pl-20 pr-10">
            <JobList jobs={jobs} />
          </div>
        </div>
      </main>
    </div>
  )
}
