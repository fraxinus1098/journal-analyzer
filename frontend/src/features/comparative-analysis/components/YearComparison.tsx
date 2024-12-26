// File: frontend/src/features/comparative-analysis/components/YearComparison.tsx
import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { LineChart } from 'recharts'
import { useComparativeData } from '../hooks/useComparativeData'
import type { ComparativeData } from '../types'

export const YearComparison = () => {
  const [selectedYears, setSelectedYears] = useState<number[]>([])
  const { data, loading } = useComparativeData(selectedYears)

  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">Year-over-Year Comparison</h2>
      {/* TODO: Implement year comparison visualization */}
    </Card>
  )
}