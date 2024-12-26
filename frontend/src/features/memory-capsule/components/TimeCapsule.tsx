// File: frontend/src/features/memory-capsule/components/TimeCapsule.tsx
import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { useMemories } from '../hooks/useMemories'
import type { Memory } from '../types'

export const TimeCapsule = () => {
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear())
  const { memories, loading } = useMemories(selectedYear)

  return (
    <Card className="p-6">
      {/* TODO: Implement memory capsule visualization */}
    </Card>
  )
}