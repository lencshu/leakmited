<script lang="ts">
  import { onMount, tick, onDestroy } from 'svelte'
  import { roadsStatsData } from '$lib/stores/roadsStore'
  import Chart from 'chart.js/auto'
  import { get } from 'svelte/store'
  import { getColorBySpeedNum } from '$lib/utils/mapping'
  import mockPieChart from '$lib/mocks/pieChart'

  let chartCanvas: HTMLCanvasElement
  let chartInstance: Chart | null = null

  onMount(async () => {
    const data = get(roadsStatsData)
    console.log('data pie', data)
    updateChart(data)
  })

  async function updateChart(data: any[]) {
    const speedCount: Record<string, number> = {}
    data.forEach((road) => {
      const sp = road.maxspeed ?? 'Unknown'
      speedCount[sp] = road.km ?? 0
    })

    const labels = Object.keys(speedCount)
    const counts = labels.map((l) => speedCount[l])

    // Destroy existing chart instance if it exists to avoid reinitialization
    if (chartInstance) {
      chartInstance.destroy()
      chartInstance = null
    }
    // waiting for DOM, then render <canvas>
    await tick()

    const backgroundColors = labels.map((l) => getColorBySpeed(l))

    chartInstance = new Chart(chartCanvas, {
      type: 'pie',
      data: {
        labels,
        datasets: [
          {
            label: 'Speed Distribution',
            data: counts,
            backgroundColor: backgroundColors,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
          },
        },
      },
    })
  }

  /**
   * color mapping according to maxspeed
   */
  function getColorBySpeed(sp: string) {
    const speed = parseInt(sp, 10)
    return getColorBySpeedNum(speed)
  }

  // Clean up chart instance on component destroy to avoid memory leaks and reinit issues
  onDestroy(() => {
    if (chartInstance) {
      chartInstance.destroy()
      chartInstance = null
    }
  })
</script>

<div class="p-4">
  <h2 class="font-bold text-lg">Pourcentage de route en km/h</h2>
  <h3 class="text-sm text-gray-600 mb-4">Donnees fourni par OpenStreetMap</h3>

  <div class="relative h-64">
    <canvas bind:this={chartCanvas} class="w-full h-full"></canvas>
  </div>
</div>
