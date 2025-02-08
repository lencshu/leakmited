<script lang="ts">
  import { onMount, tick } from 'svelte'
  import SpeedFilter from '$lib/components/SpeedFilter.svelte'
  import SpeedPieChart from '$lib/components/SpeedPieChart.svelte'
  import MapRoads from '$lib/components/MapRoads.svelte'
  import Loading from '$lib/components/Loading.svelte'
  import { fetchRoadsStats } from '$lib/utils/api'
  import { roadsStatsData } from '$lib/stores/roadsStore'
  import { get } from 'svelte/store'

  let pageLoading = true
  let mapLoading = false

  onMount(async () => {
    const storedRoadsStats = get(roadsStatsData)
    if (storedRoadsStats.length === 0) {
      const dataStats = await fetchRoadsStats()
      roadsStatsData.set(dataStats)
    }

    pageLoading = false
  })

  function handleLoadingStart() {
    mapLoading = true
  }
  function handleLoadingEnd() {
    mapLoading = false
  }
</script>

{#if pageLoading}
  <div class="mt-20"><Loading message="Loading..." /></div>
{:else}
  <div class="container mx-auto p-3">
    <h1 class="text-center text-3xl font-bold mb-6">Carte de l'IDF</h1>
    <div class="flex gap-6" style="height: 600px;">
      <div class="w-1/3 flex flex-col gap-6 h-full">
        <div class="p-4 bg-white border border-gray-300 rounded-lg shadow basis-1/3">
          <SpeedFilter onLoadingStart={handleLoadingStart} onLoadingEnd={handleLoadingEnd} />
        </div>
        <div class="p-4 bg-white border border-gray-300 rounded-lg shadow basis-2/3">
          <SpeedPieChart />
        </div>
      </div>

      <div class="w-2/3 p-4 bg-white border border-gray-300 rounded-lg shadow">
        {#if mapLoading}
          <Loading message="Loading roads data..." />
        {:else}
          <MapRoads />
        {/if}
      </div>
    </div>
  </div>
{/if}
