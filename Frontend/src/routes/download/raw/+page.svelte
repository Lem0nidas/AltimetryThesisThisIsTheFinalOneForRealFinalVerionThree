<script lang="ts">
	let selectedSatellite = '';
	let responseMessage = '';

	const satellites = [
		{ name: 'Geosat', code: 'gs' },
		{ name: 'ERS-1', code: 'e1' },
		{ name: 'TOPEX', code: 'tx' },
		{ name: 'Poseidon', code: 'pn' },
		{ name: 'ERS-2', code: 'e2' },
		{ name: 'GFO', code: 'g1' },
		{ name: 'Jason-1', code: 'j1' },
		{ name: 'Envisat', code: 'n1' },
		{ name: 'Jason-2', code: 'j2' },
		{ name: 'CryoSat-2', code: 'c2' },
		{ name: 'SARAL', code: 'sa' },
		{ name: 'Jason-3', code: 'j3' },
		{ name: 'Sentinel-3A', code: '3a' },
		{ name: 'Sentinel-3B', code: '3b' },
		{ name: 'Sentinel-6A', code: '6a' },
		{ name: 'SWOT nadir', code: 'sw' }
	];

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		if (!selectedSatellite) {
			responseMessage = 'Please select a satellite.';
			return;
		}

		try {
			const resA = await fetch('http://localhost:8000/api/download', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ satellite: selectedSatellite })
			});

			const dataA = await resA.json();
			responseMessage = dataA.message || 'First Request sent!';

			const resB = await fetch('http://localhost:8000/api/download_latest', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ satellite: selectedSatellite })
			});

			const dataB = await resB.json();
			responseMessage = dataB.message || 'File Downloaded!';
		} catch (err) {
// TODO I get the error message even if the request is successful, need to fix this
			responseMessage = 'Error contacting server.';
			console.error(err);
		}
	}
</script>

<h1>
    Welcome to Download Raw Data page
</h1>

<form on:submit={handleSubmit}>
	<label for="satellite">Choose a satellite:</label>
	<select id="satellite" bind:value={selectedSatellite} required>
		<option value="" disabled selected>Select one</option>
		{#each satellites as sat}
			<option value={sat.code}>{sat.name}</option>
		{/each}
	</select>

	<button type="submit">Submit</button>
</form>

{#if responseMessage}
	<p>{responseMessage}</p>
{/if}
