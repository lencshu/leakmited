<script lang="ts">
  import { onMount, tick } from 'svelte'
  import { fetchStats } from '$lib/utils/api' // 预留 API 访问函数
  import Chart from 'chart.js/auto'
  import Loading from '$lib/components/Loading.svelte'
  // import mockStats from '$lib/mocks/stats'

  let totalLength: number = 0
  let speedDistribution: Record<string, number> = {}

  let chartContainer: HTMLCanvasElement
  let myChart: Chart | null = null

  let isLoading = true

  onMount(async () => {
    const stats = await fetchStats()
    // const stats = mockStats

    totalLength = stats.total_length
    speedDistribution = stats.speed_distribution

    isLoading = false

    // waiting for DOM, then render <canvas>
    await tick()

    const labels = Object.keys(speedDistribution)
    const values = Object.values(speedDistribution)

    myChart = new Chart(chartContainer, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Road Length Distribution (km)',
            data: values,
            backgroundColor: ['#EF4444', '#F59E0B', '#10B981', '#3B82F6'],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    })
  })
</script>

{#if isLoading}
  <div class="mt-20"><Loading message="Loading..." /></div>
{:else}
  <div class="container mx-auto p-3">
    <h1 class="text-center text-3xl font-bold mb-6">Dashboard Statistics</h1>
    <div class="flex gap-6">
      <div class="w-1/3 bg-white rounded-lg shadow p-6 flex flex-col justify-center items-center">
        <h2 class="text-xl font-bold mb-4">Total length of the road network</h2>
        <p class="text-4xl font-semibold text-blue-600">{totalLength.toFixed(2)} km</p>
      </div>
      <div class="w-2/3 bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">Road Length Distribution by Max Speed (km/h)</h2>
        <div class="h-96">
          <canvas bind:this={chartContainer} class="w-full h-full"></canvas>
        </div>
      </div>
    </div>
  </div>
{/if}
