<script lang="ts">
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';
	import { onMount } from 'svelte';
	import simplified_oceans from '$lib/data/simplified_oceans.geojson?raw';

	let mapContainer: HTMLDivElement;
	let map: L.Map;
	let geojasonLayer: L.GeoJSON;
	let selectedOcean = $state('');
	let oceanNames: string[] = $state([]);
	let parsedGeoJson = JSON.parse(simplified_oceans);

	function highlightOcean(name: string) {
		geojasonLayer.eachLayer((layer: any) => {
			if (layer.feature?.properties?.name === name) {
				map.fitBounds(layer.getBounds());
				layer.setStyle({
					color: 'blue',
					weight: 2,
					fillOpacity: 0.5
				});
			} else {
				geojasonLayer.resetStyle(layer);
			}
		});
	}

	onMount(() => {
		map = L.map(mapContainer, {
			maxBounds: [
				[-85, -180],
				[85, 180]
			],
			maxBoundsViscosity: 0.9,
			zoomControl: false
		}).setView([10, 0], 2);
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			noWrap: true,
			maxZoom: 5,
			minZoom: 2
		}).addTo(map);

		geojasonLayer = L.geoJSON(parsedGeoJson, {
			style: {
				color: 'gray',
				weight: 1,
				fillOpacity: 0.3
			},
			onEachFeature: (feature, layer) => {
				const name = feature.properties?.name || 'Unknown';
				oceanNames.push(name);

				layer.on('click', (e) => {
					const { lat, lng } = e.latlng;
					alert(`Clicked: ${name}\nLat: ${lat.toFixed(2)}, Lon: ${lng.toFixed(2)}`);
				});
			}
		});

		geojasonLayer.addTo(map);
	});
</script>

<div>
	<label for="">Select an ocean: </label>
	<select bind:value={selectedOcean} onchange={() => highlightOcean(selectedOcean)}>
		<option disabled selected value="">-- Choose --</option>
		{#each [...new Set(oceanNames)] as name}
			<option value={name}>{name}</option>
		{/each}
	</select>
</div>

<div bind:this={mapContainer} id="map"></div>

<style>
	#map {
		height: 500px;
		width: 50%;
		margin: 1rem auto 2rem;
		border: 1px solid #2a3140;
		border-radius: 20px;
		position: relative;
	}

	div {
		width: 45%;
		margin: auto;
	}
</style>
