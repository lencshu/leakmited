export async function fetchStats() {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/stats`)
  if (!response.ok) {
    throw new Error('Failed to fetch stats')
  }
  return response.json()
}

export async function fetchRoadsStats() {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/roads-statistics`)
  if (!response.ok) {
    throw new Error('Failed to fetch stats')
  }
  return response.json()
}

export async function fetchRoadsBySpeed(maxSpeed: number) {
  const url = `${import.meta.env.VITE_API_BASE_URL}/roads/?max_speed=${maxSpeed}`
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error('Failed to fetch roads')
  }
  return response.json()
}
