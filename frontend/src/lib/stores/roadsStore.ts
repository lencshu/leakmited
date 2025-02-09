import { writable } from 'svelte/store'

// all speed limit selected（30,50,70,90）
export const selectedSpeeds = writable<Set<number>>(new Set())

// an array of objects or GeoJSON Features representing the filtered roads
export const roadsData = writable<any[]>([])

// statistics returned by the backend
export const roadsStatsData = writable<any[]>([])
