import type { StatsBase } from '$lib/types/stats'
import { writable } from 'svelte/store'

export const statsData = writable<StatsBase>()
