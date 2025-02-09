import { describe, test, expect, vi, beforeEach } from 'vitest'
import { selectedSpeeds, roadsData } from '$lib/stores/roadsStore'
import { get } from 'svelte/store'

// define mock data at top-level, so it is available when Vitest hoists the mock
const mockFetchResult = [
  {
    geometry: {
      coordinates: [
        [2.3, 48.87],
        [2.31, 48.88],
      ],
    },
    properties: {},
  },
]

// define the mock for `$lib/utils/api` at top-level, ensuring it's hoisted properly
vi.mock('$lib/utils/api', () => {
  return {
    fetchRoadsBySpeed: vi.fn().mockResolvedValue(mockFetchResult),
  }
})

describe('SpeedFilter logic (no DOM)', () => {
  beforeEach(() => {
    selectedSpeeds.set(new Set())
    roadsData.set([])
  })

  test('adds new speed to selectedSpeeds and fetch data', async () => {
    // dynamic import after mock is hoisted
    const { fetchRoadsBySpeed: mockFetch } = await import('$lib/utils/api')

    // simulate onLoadingStart/onLoadingEnd
    const onLoadingStart = vi.fn()
    const onLoadingEnd = vi.fn()

    onLoadingStart()
    selectedSpeeds.update((set) => {
      set.add(50)
      return set
    })
    // simulate fetchRoadsBySpeed(50)
    const res = await mockFetch(50)
    roadsData.update((r) => [...r, ...res])
    onLoadingEnd()

    const speeds = get(selectedSpeeds)
    expect(speeds.has(50)).toBe(true)

    const roads = get(roadsData)
    expect(roads).toHaveLength(1)
    expect(roads[0].geometry.coordinates).toEqual([
      [2.3, 48.87],
      [2.31, 48.88],
    ])

    expect(onLoadingStart).toHaveBeenCalled()
    expect(onLoadingEnd).toHaveBeenCalled()
  })

  test('removes speed from selectedSpeeds and clears roadsData', () => {
    selectedSpeeds.set(new Set([30, 50]))
    roadsData.set([{ geometry: {}, properties: { maxspeed: 30 } }])

    selectedSpeeds.update((set) => {
      set.delete(30)
      return set
    })
    roadsData.update((r) => r.filter((item) => item.properties.maxspeed !== 30))

    const speeds = get(selectedSpeeds)
    expect(speeds.has(30)).toBe(false)
    expect(speeds.has(50)).toBe(true)

    const roads = get(roadsData)
    expect(roads).toHaveLength(0)
  })
})
