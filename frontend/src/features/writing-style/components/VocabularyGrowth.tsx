// File: frontend/src/features/writing-style/components/VocabularyGrowth.tsx
import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { useVocabularyData } from '../hooks/useVocabularyData'
import type { VocabularyData } from '../types'

export const VocabularyGrowth = () => {
  const [period, setPeriod] = useState<'6months' | '1year' | 'all'>('1year')
  const { data, loading } = useVocabularyData(period)

  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">Vocabulary Growth</h2>
      {/* TODO: Implement vocabulary growth visualization */}
    </Card>
  )
}