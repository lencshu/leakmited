<script lang="ts">
  import { selectedSpeeds, roadsData } from '$lib/stores/roadsStore'
  import { fetchRoadsBySpeed } from '$lib/utils/api'
  import { get } from 'svelte/store'
  import { getColorBySpeedNum } from '$lib/utils/mapping'

  // use callback props instead of createEventDispatcher
  export let onLoadingStart: () => void = () => {}
  export let onLoadingEnd: () => void = () => {}

  const speedOptions = [
    { label: '30 km/h', value: 30, color: getColorBySpeedNum(30) },
    { label: '50 km/h', value: 50, color: getColorBySpeedNum(50) },
    { label: '70 km/h', value: 70, color: getColorBySpeedNum(70) },
    { label: '90 km/h', value: 90, color: getColorBySpeedNum(90) },
  ]

  /**
   * When the checkbox changes, update the selected speed limits and fetch road data
   * @param {number} value speed value
   */
  async function onCheckboxChange(value: number) {
    const currentSet = new Set(get(selectedSpeeds))
    if (currentSet.has(value)) {
      currentSet.delete(value)
    } else {
      currentSet.add(value)
    }
    selectedSpeeds.set(currentSet)
    // Call callback prop for loading start
    onLoadingStart()
    await fetchSelectedRoads()
    // Call callback prop for loading end
    onLoadingEnd()
  }

  async function fetchSelectedRoads() {
    const speedsArray = Array.from(get(selectedSpeeds))
    if (speedsArray.length === 0) {
      roadsData.set([])
      return
    }
    let allRoads: any[] = []
    for (let sp of speedsArray) {
      const res = await fetchRoadsBySpeed(sp)
      allRoads = allRoads.concat(res)
    }
    roadsData.set(allRoads)
  }
</script>

<div class="p-4">
  <h2 class="font-bold text-lg">Filter les routes par limitation de vitesse</h2>
  <h3 class="text-sm text-gray-600 mb-4">Données fourni par OpenStreetMap</h3>

  <div class="flex space-x-3">
    {#each speedOptions as opt}
      <div class="flex flex-col items-center">
        <label class="flex items-center space-x-1">
          <input type="checkbox" value={opt.value} on:change={() => onCheckboxChange(opt.value)} />
          <span class="text-sm">{opt.label}</span>
        </label>
        <div class="mt-1 w-12 h-3 rounded-full" style="background-color: {opt.color};"></div>
      </div>
    {/each}
  </div>
</div>
