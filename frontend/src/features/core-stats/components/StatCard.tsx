/**
 * Component for displaying individual statistics in a card format.
 * File: frontend/src/features/core-stats/components/StatCard.tsx
 */

import { Card } from '@/components/ui/card'
import type { StatCardProps } from '../types'

export interface StatCardProps {
  title: string
  value: string | number
  description?: string
  trend?: {
    direction: 'up' | 'down' | 'neutral'
    percentage: number
  }
}

export const StatCard = ({ title, value, description, trend }: StatCardProps) => {
  return (
    <Card className="p-4">
      {/* TODO: Implement stat card visualization with:
          - Title
          - Value display
          - Optional description
          - Optional trend indicator
      */}
    </Card>
  )
}
