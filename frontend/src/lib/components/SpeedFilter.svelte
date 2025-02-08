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
    const wasPresent = currentSet.has(value)

    // if the value was already present, remove it; otherwise, add it
    if (wasPresent) {
      currentSet.delete(value)
      removeRoadsData(value) // remove data related to the deselected speed
    } else {
      currentSet.add(value)
      await fetchNewRoadsData(value) // only fetch new data for newly selected speed
    }

    selectedSpeeds.set(currentSet)
  }

  // function to fetch only the new roads data when a new speed is selected
  async function fetchNewRoadsData(speed: number) {
    onLoadingStart()

    const res = await fetchRoadsBySpeed(speed)
    const processedData = res.map((road: any) => {
      // modify the returned data structure
      return {
        geometry: {
          type: 'LineString',
          coordinates: road.geometry.coordinates,
        },
        properties: {
          maxspeed: speed,
        },
      }
    })

    // add only new data
    roadsData.update((currentData) => [...currentData, ...processedData])

    onLoadingEnd()
  }

  // remove the data related to a deselected speed from the store
  function removeRoadsData(speed: number) {
    roadsData.update((currentData) => currentData.filter((road) => road.properties.maxspeed !== speed))
  }
</script>

<div class="p-4">
  <h2 class="font-bold text-lg">Filter les routes par limitation de vitesse</h2>
  <h3 class="text-sm text-gray-600 mb-4">Données fourni par OpenStreetMap</h3>

  <div class="flex space-x-3">
    {#each speedOptions as opt}
      <div class="flex flex-col items-center">
        <label class="flex items-center space-x-1">
          <!-- Bind the checkbox's checked attribute -->
          <input type="checkbox" value={opt.value} checked={$selectedSpeeds.has(opt.value)} on:change={() => onCheckboxChange(opt.value)} />
          <span class="text-sm">{opt.label}</span>
        </label>
        <div class="mt-1 w-12 h-3 rounded-full" style="background-color: {opt.color};"></div>
      </div>
    {/each}
  </div>
</div>
