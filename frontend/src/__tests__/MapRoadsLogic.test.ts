import { describe, test, expect } from 'vitest'
import { getColorBySpeedNum } from '$lib/utils/mapping'

describe('MapRoads logic (no DOM)', () => {
  test('getColorBySpeedNum mapping', () => {
    expect(getColorBySpeedNum(30)).toBe('#EF4444')
    expect(getColorBySpeedNum(50)).toBe('#F59E0B')
    expect(getColorBySpeedNum(70)).toBe('#10B981')
    expect(getColorBySpeedNum(90)).toBe('#3B82F6')
    expect(getColorBySpeedNum(999)).toBe('#999999')
  })
})
