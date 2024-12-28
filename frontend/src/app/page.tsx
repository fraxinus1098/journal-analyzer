import { UploadForm } from '@/components/UploadForm'

export default function Home() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Journal Analyzer</h1>
      <UploadForm />
    </main>
  )
}
