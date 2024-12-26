// File: frontend/src/features/personal-growth/components/GoalTracker.tsx
import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { useGoals } from '../hooks/useGoals'
import { GoalProgress } from './GoalProgress'
import type { Goal } from '../types'

export const GoalTracker = () => {
  const [timeframe, setTimeframe] = useState<'month' | 'quarter' | 'year'>('year')
  const { goals, loading } = useGoals(timeframe)

  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">Goal Tracking</h2>
      {/* TODO: Implement goal tracking visualization */}
    </Card>
  )
}