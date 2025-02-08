<script lang="ts">
  import L from 'leaflet'
  import { onMount } from 'svelte'
  import { roadsData } from '$lib/stores/roadsStore'
  import { getColorBySpeedNum } from '$lib/utils/mapping'

  import mockRoads from '$lib/mocks/roads'

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

    // add OSM photo layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
    }).addTo(map)

    // roadsData.set(mockRoads)

    // subscribe to roadsData
    const unsubscribe = roadsData.subscribe((data) => {
      if (roadsLayer) {
        roadsLayer.remove()
        roadsLayer = null
      }
      if (!data || data.length === 0) return

      // GeoJSON FeatureCollection
      const geojsonData = {
        type: 'FeatureCollection',
        features: data.map((item) => ({
          type: 'Feature',
          geometry: item.geometry,
          properties: item.properties,
        })),
      }

      roadsLayer = L.geoJSON(geojsonData, {
        style: styleFeature,
        onEachFeature: (feature, layer) => {
          // tooltip
          layer.on('click', () => {
            const maxSpeed = feature.properties?.maxspeed || 'Unknown'
            const highway = feature.properties?.highway || 'Unknown'
            const osmId = feature.properties?.osm_id || 'Unknown'
            const contentStr = `<b>Max Speed:</b> ${maxSpeed} km/h</br><b>Type</b>: ${highway}</br><b>osmId</b>: ${osmId}`
            L.popup().setLatLng(layer.getBounds().getCenter()).setContent(contentStr).openOn(map)
          })
        },
      }).addTo(map)
    })

    return () => {
      unsubscribe()
      map.remove()
    }
  })

  /**
   * color mapping
   */
  function styleFeature(feature: any) {
    const speed = feature.properties?.maxspeed
    const color = getColorBySpeedNum(speed)
    return { color, weight: 4 }
  }
</script>

<div id="mapid" class="w-full h-full relative overflow-hidden"></div>
