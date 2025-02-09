import type { StatsBase } from '$lib/types/stats'
import { writable } from 'svelte/store'

//  statistics returned by the backend (total length, distribution, etc.).
export const statsData = writable<StatsBase>()
