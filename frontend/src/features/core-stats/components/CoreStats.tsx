// File: frontend/src/features/core-stats/components/CoreStats.tsx
import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { useStats } from '../hooks/useStats'
import type { CoreStatsData } from '../types'

export const CoreStats = () => {
  const [timeRange, setTimeRange] = useState('year')
  const { data, loading } = useStats(timeRange)
  
  return (
    <Card className="p-6">
      {/* TODO: Implement core stats visualization */}
    </Card>
  )
}