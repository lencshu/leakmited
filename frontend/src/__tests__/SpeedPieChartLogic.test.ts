import { describe, test, expect, beforeEach } from 'vitest'
import { roadsData } from '$lib/stores/roadsStore'
import { get } from 'svelte/store'

describe('SpeedPieChart logic (no DOM)', () => {
  beforeEach(() => {
    roadsData.set([])
  })

  test('stores roads data for pie chart usage', () => {
    roadsData.set([
      {
        geometry: { coordinates: [] },
        properties: { maxspeed: 30 },
      },
      {
        geometry: { coordinates: [] },
        properties: { maxspeed: 50 },
      },
      {
        geometry: { coordinates: [] },
        properties: { maxspeed: 30 },
      },
    ])

    const data = get(roadsData)
    expect(data).toHaveLength(3)

    // Mock stats：2 for maxspeed=30， 1 for 50
    const speedCount: Record<string, number> = {}
    data.forEach((road) => {
      const sp = road.properties.maxspeed
      speedCount[sp] = (speedCount[sp] || 0) + 1
    })
    expect(speedCount[30]).toBe(2)
    expect(speedCount[50]).toBe(1)
  })
})
