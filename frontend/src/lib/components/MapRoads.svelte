<script lang="ts">
  import L from 'leaflet'
  import { onMount, tick } from 'svelte'
  import { roadsData } from '$lib/stores/roadsStore'
  import { getColorBySpeedNum } from '$lib/utils/mapping'

  import mockRoads from '$lib/mocks/roads'
  import { debounce } from 'lodash'

  let map: L.Map
  let roadsLayer: L.GeoJSON<any> | null = null

  onMount(() => {
    map = L.map('mapid', {
      center: [48.8566, 2.3522],
      zoom: 11,
      zoomControl: false,
    })

    L.control
      .zoom({
        position: 'topleft',
      })
      .addTo(map)

    // Add OSM tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
    }).addTo(map)

    // Use roadsData to dynamically load GeoJSON data
    const unsubscribe = roadsData.subscribe((data) => {
      if (roadsLayer) {
        roadsLayer.remove()
        roadsLayer = null
      }

      if (!data || data.length === 0) return

      // Initialize geoJSON with filtered data based on map bounds
      const geojsonData = {
        type: 'FeatureCollection',
        features: data.map((item) => ({
          type: 'Feature',
          geometry: item.geometry,
          properties: item.properties,
        })),
      }

      // Use leaflet's cluster feature to handle large datasets efficiently
      roadsLayer = L.geoJSON(geojsonData, {
        style: styleFeature,
        onEachFeature: (feature, layer) => {
          layer.on('click', () => {
            const maxSpeed = feature.properties?.maxspeed || 'Unknown'
            const contentStr = `<b>Max Speed:</b> ${maxSpeed} km/h`
            L.popup().setLatLng(layer.getBounds().getCenter()).setContent(contentStr).openOn(map)
          })
        },
      }).addTo(map)

      // Debounce the update of displayed data on zoom or move
      map.on(
        'moveend',
        debounce(() => {
          updateVisibleData(map, geojsonData.features)
        }, 200)
      )
    })

    return () => {
      unsubscribe()
      map.remove()
    }
  })

  /**
   * color mapping based on speed
   */
  function styleFeature(feature: any) {
    const speed = feature.properties?.maxspeed
    const color = getColorBySpeedNum(speed)
    return { color, weight: 4 }
  }

  // Update data visible in the current map bounds
  function updateVisibleData(map: L.Map, allFeatures: any[]) {
    const bounds = map.getBounds()
    const filteredFeatures = allFeatures.filter((feature: any) => {
      const latlngs = feature.geometry.coordinates
      return latlngs.some((coord: any) => bounds.contains(L.latLng(coord[1], coord[0])))
    })

    // Create GeoJSON with visible features only
    const visibleGeoJson = {
      type: 'FeatureCollection',
      features: filteredFeatures,
    }

    // Remove existing roadsLayer and add new one based on the visible data
    if (roadsLayer) {
      roadsLayer.clearLayers()
      L.geoJSON(visibleGeoJson, {
        style: styleFeature,
        onEachFeature: (feature, layer) => {
          layer.on('click', () => {
            const maxSpeed = feature.properties?.maxspeed || 'Unknown'
            const contentStr = `<b>Max Speed:</b> ${maxSpeed} km/h`
            L.popup().setLatLng(layer.getBounds().getCenter()).setContent(contentStr).openOn(map)
          })
        },
      }).addTo(map)
    }
  }
</script>

<div id="mapid" class="w-full h-full relative overflow-hidden"></div>
