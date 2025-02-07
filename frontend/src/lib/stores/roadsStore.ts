import { writable } from 'svelte/store'

// all speed limit selected（30,50,70,90）
export const selectedSpeeds = writable<Set<number>>(new Set())

export const roadsData = writable<any[]>([])
