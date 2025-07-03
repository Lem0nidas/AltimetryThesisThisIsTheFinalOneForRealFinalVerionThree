
<script lang="ts">
    import L from 'leaflet';
    import 'leaflet/dist/leaflet.css';
    import { onMount } from 'svelte';
    import countries from '$lib/data/countries.geojson?raw'

    let mapContainer: HTMLDivElement
    let map: L.Map
    let geojasonLayer: L.GeoJSON;
    let selectedCountry = '';
    let countryNames: string[] = [];
    let parsedGeoJson = JSON.parse(countries);

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
                geojasonLayer.resetStyle(layer)
            }
        });
    }


    onMount(() => {
        map = L.map(mapContainer).setView([10, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        geojasonLayer = L.geoJSON(parsedGeoJson, {
            style: {
                color: 'gray',
                weight: 1,
                fillOpacity: 0.3
            },
            onEachFeature: (feature, layer) => {
                const name = feature.properties?.name || 'Unknown';
                countryNames.push(name);

                layer.on('click', (e) => {
                    const { lat, lng } = e.latlng;
                    alert(`Clicked: ${name}\nLat: ${lat.toFixed(2)}, Lon: ${lng.toFixed(2)}`);
                });
            }
        });

        geojasonLayer.addTo(map);
    })
</script>

<style>
    #map {
        height: 500px;
        width: 100%;
    }
</style>

<div>
    <label for="">Select a country: </label>
    <select bind:value={selectedCountry} onchange={() => highlightOcean(selectedCountry)}>
        <option disabled selected value="">--- Choose --</option>
        {#each [...new Set(countryNames)] as name}
            <option value={name}>{name}</option>
        {/each}
    </select>
</div>

<div bind:this={mapContainer} id="map"></div>