<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import 'leaflet/dist/leaflet.css';
	import L, { Bounds, LatLng, Rectangle as LeafletRectangle } from 'leaflet';
	import simplified_oceans from '$lib/data/simplified_oceans.geojson?raw';
	import { requestBox } from '$lib/api/map';

	let map: L.Map;
	let geojsonLayer: L.GeoJSON;
	let mapContainer: HTMLDivElement;
	let { selectedArea = $bindable() }: { selectedArea: string } = $props();
	let areaNames: string[] = $state(['']);
	let parsedGeoJson = JSON.parse(simplified_oceans);
	let mode: 'ocean' | 'draw' = $state('ocean');

	let startPoint: LatLng | null;
	let rectangle: LeafletRectangle;
	let bounds: [L.LatLngTuple, L.LatLngTuple];

	let isMoving = false;
	let moveOffset: L.LatLng | null = null;

	function handleToggle(e: Event) {
		const checked = (e.target as HTMLInputElement).checked;
		setMode(checked ? 'draw' : 'ocean');
	}

	function enableDrawMode() {
		map.dragging.disable();
		map.getContainer().style.cursor = 'crosshair';
		map.on('mousedown', onMouseDown);
	}

	function disableDrawMode() {
		map.dragging.enable();
		map.getContainer().style.cursor = '';
		rectangle?.remove();
		map.off('mousedown', onMouseDown);
		map.off('mousemove', onMouseMove);
		map.off('mousemove', onRectangleMove);
	}

	function enableOceanMode() {
		addOceansLayer();
	}

	function disableOceanMode() {
		geojsonLayer?.remove();
	}

	function setMode(newMode: 'ocean' | 'draw') {
		if (mode === newMode) return;

		if (mode === 'draw') disableDrawMode();
		if (mode === 'ocean') disableOceanMode();

		mode = newMode;

		if (mode === 'draw') enableDrawMode();
		if (mode === 'ocean') enableOceanMode();
	}

	function addOceansLayer() {
		geojsonLayer = L.geoJSON(parsedGeoJson, {
			style: {
				color: 'gray',
				weight: 1,
				fillOpacity: 0.3
			},
			onEachFeature: (feature, layer) => {
				const name = feature.properties?.name || 'Unknown';
				if (!areaNames.includes(name)) {
					areaNames = [...areaNames, name];
				}

				layer.on('click', () => {
					selectedArea = name;
					highlightOcean(name);
				});
			}
		});
		geojsonLayer.addTo(map);
	}

	function highlightOcean(name: string) {
		geojsonLayer.eachLayer((layer: any) => {
			if (layer.feature?.properties?.name === name) {
				map.fitBounds(layer.getBounds());
				layer.setStyle({
					color: 'blue',
					weight: 2,
					fillOpacity: 0.5
				});
			} else {
				geojsonLayer.resetStyle(layer);
			}
		});
	}

	function onMouseDown(e: L.LeafletMouseEvent) {
		startPoint = e.latlng;
		if (e.originalEvent.ctrlKey || e.originalEvent.button === 1) {
			map.dragging.enable();
			return;
		}

		map.dragging.disable();

		if (rectangle && rectangle.getBounds().contains(e.latlng)) {
			isMoving = true;

			const bounds = rectangle.getBounds();
			moveOffset = L.latLng(
				e.latlng.lat - bounds.getSouthWest().lat,
				e.latlng.lng - bounds.getSouthWest().lng
			);

			map.on('mousemove', onRectangleMove);
			map.once('mouseup', onEndMove);
			return;
		} else {
			rectangle?.remove();

			const initialBounds: [L.LatLngTuple, L.LatLngTuple] = [
				[startPoint.lat, startPoint.lng],
				[startPoint.lat, startPoint.lng]
			];

			rectangle = L.rectangle(initialBounds, {
				color: '#ff0008',
				weight: 1
			}).addTo(map);

			map.on('mousemove', onMouseMove);
			map.once('mouseup', onMouseUp);
		}
	}

	function onMouseMove(e: L.LeafletMouseEvent) {
		if (!startPoint || !rectangle) return;

		bounds = [
			[startPoint.lat, startPoint.lng],
			[e.latlng.lat, e.latlng.lng]
		];

		if (rectangle) rectangle.setBounds(bounds);
	}

	function onMouseUp() {
		map.off('mousemove', onMouseMove);
		if (rectangle) {
			selectedArea = getBoundsString(rectangle);
		}
		startPoint = null;
	}

	function onRectangleMove(e: L.LeafletMouseEvent) {
		if (!rectangle || !isMoving || !moveOffset) return;

		const bounds = rectangle.getBounds();
		const sw = bounds.getSouthWest();
		const ne = bounds.getNorthEast();

		const latDiff = e.latlng.lat - sw.lat - moveOffset.lat;
		const lngDiff = e.latlng.lng - sw.lng - moveOffset.lng;

		const newSw = L.latLng(sw.lat + latDiff, sw.lng + lngDiff);
		const newNe = L.latLng(ne.lat + latDiff, ne.lng + lngDiff);

		rectangle.setBounds(L.latLngBounds(newSw, newNe));
	}

	function onEndMove() {
		isMoving = false;
		moveOffset = null;
		map.off('mousemove', onRectangleMove);
		map.dragging.enable();

		if (rectangle) {
			selectedArea = getBoundsString(rectangle);
		}
	}

	function getBoundsString(rectangle: L.Rectangle<any>) {
		const bounds = rectangle.getBounds();
		const sw = bounds.getSouthWest();
		const ne = bounds.getNorthEast();

		return [sw.lng.toFixed(2), ne.lng.toFixed(2), sw.lat.toFixed(2), ne.lat.toFixed(2)].join(',');
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

		setMode(mode);
	});

	onDestroy(() => {
		map?.remove();
	});
</script>

<div>
	<fieldset id="map-type">
		<label for="map-type-switch">
			Ocean
			<input id="map-type-switch" type="checkbox" role="switch" onchange={handleToggle} />
			Select
		</label>
	</fieldset>

	<label for="area-select">Select an area: </label>
	<select id="area-select" bind:value={selectedArea} onchange={() => highlightOcean(selectedArea)}>
		<option disabled selected value="">-- Choose --</option>
		{#each [...new Set(areaNames)] as name}
			<option value={name}>{name}</option>
		{/each}
	</select>
</div>

<p>Mode: {mode}</p>
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
