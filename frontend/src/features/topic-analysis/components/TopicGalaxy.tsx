// File: frontend/src/features/topic-analysis/components/TopicGalaxy.tsx
import { useEffect, useRef } from 'react'
import * as THREE from 'three'
import { useTopicData } from '../hooks/useTopicData'

export const TopicGalaxy = () => {
  const containerRef = useRef<HTMLDivElement>(null)
  const { data, loading } = useTopicData()

  useEffect(() => {
    // TODO: Implement Three.js visualization
  }, [data])

  return <div ref={containerRef} className="w-full h-[600px]" />
}
