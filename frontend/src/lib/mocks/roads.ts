const mockRoads = [
  {
    geometry: {
      type: 'LineString',
      // 注意：GeoJSON 坐标格式为 [经度, 纬度]
      coordinates: [
        [2.295, 48.8738], // Arc de Triomphe
        [2.3, 48.871],
        [2.305, 48.868],
      ],
    },
    properties: {
      maxspeed: 50,
      highway: 'residential',
      osm_id: 165436231,
    },
  },
  {
    geometry: {
      type: 'LineString',
      coordinates: [
        [2.305, 48.868],
        [2.31, 48.867],
        [2.315, 48.866],
        [2.3212, 48.8656], // Place de la Concorde
      ],
    },
    properties: {
      maxspeed: 70,
      highway: 'residential',
      osm_id: 165436231,
    },
  },
  {
    geometry: {
      type: 'LineString',
      coordinates: [
        [2.3522, 48.8566],
        [2.3622, 48.8566],
        [2.3722, 48.8566],
      ],
    },
    properties: {
      maxspeed: 50,
      highway: 'residential',
      osm_id: 165436231,
    },
  },
  {
    geometry: {
      type: 'LineString',
      coordinates: [
        [2.3522, 48.8566],
        [2.3522, 48.8666],
        [2.3522, 48.8766],
      ],
    },
    properties: {
      maxspeed: 70,
      highway: 'residential',
      osm_id: 165436231,
    },
  },
  {
    geometry: {
      type: 'LineString',
      coordinates: [
        [2.3622, 48.8566],
        [2.3722, 48.8666],
        [2.3822, 48.8766],
      ],
    },
    properties: {
      maxspeed: 90,
      highway: 'residential',
      osm_id: 165436231,
    },
  },
]

export default mockRoads
