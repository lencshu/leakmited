/**
 * color mapping according to maxspeed
 */
export function getColorBySpeedNum(sp: number) {
  switch (sp) {
    case 30:
      return '#EF4444'
    case 50:
      return '#F59E0B'
    case 70:
      return '#10B981'
    case 90:
      return '#3B82F6'
    default:
      return '#999999'
  }
}
