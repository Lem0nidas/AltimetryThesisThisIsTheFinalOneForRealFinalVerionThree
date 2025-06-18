<!-- TODO CLEAN UP THE SCRIPT -->

<script lang="ts">
	import { requestCustomDownload, requestDownload, requestLatestDownload, requestDateDownload } from "$lib/api/rads";
	import { Satellite } from "@lucide/svelte";

	let selectedSatellite = $state('');
	let selectedCycle = $state('');
	let responseMessage = $state('');
	let downloadMessage = $state('');
	let customMessage = $state('');
	let errorMessage = $state('');
	let dateMessage = $state('');

	let toggles = $state({
		a: false,
		b: false
	});
	
	let selectedPass = $derived.by(() => {
		if (!toggles.a) {
			return '';
		}
	});

	let selectedDate = $derived.by(() => {
		if (!toggles.b) return 'Date not selected';
	});


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

		if (!selectedDate) {
			console.log('Please pick a date')
		}
		// console.log(typeof selectedDate)

		try {
			// responseMessage = await requestDownload(selectedSatellite);
			// downloadMessage = await requestLatestDownload(selectedSatellite);
			// customMessage = await requestCustomDownload(selectedSatellite, selectedCycle, selectedPass);
			dateMessage = await requestDateDownload(selectedSatellite, selectedDate);
		} catch (err) {
			errorMessage = 'Error contacting server.';
			console.error(err);
		}
	}
</script>

<h1>
    Welcome to Download Raw Data page
</h1>

<form onsubmit={handleSubmit}>
	<fieldset>
		<label for="satellite">Choose a satellite:</label>
		<select id="satellite" bind:value={selectedSatellite} required>
			<option value="" disabled selected>Select one</option>
			{#each satellites as sat}
				<option value={sat.code}>{sat.name}</option>
			{/each}
		</select>
	</fieldset>

	<fieldset>
		<label for="cycle">Type the cycle number:</label>
		<input type="text" id="cycle" bind:value={selectedCycle} placeholder="e.g. 015" />
	</fieldset>

	<fieldset>
		<label for="pass-switch">
			<input type="checkbox" id="pass-switch" name="pass-switch" role="switch" bind:checked={toggles.a} />
			Pick Specific Pass
		</label>
		{#if toggles.a}
			<label for="pass">Type the pass number:</label>
			<input type="text" id="pass" bind:value={selectedPass} placeholder="e.g. 0234" />
		{/if}
	</fieldset>

	<!-- TODO Create a date based download settings, logic, backed, EVERYTHING -->
	<!-- TODO First make the download by date possible -->
	<fieldset>
		<label for="start-date-switch">
			<input type="checkbox" id="start-date-switch" name="start-date-switch" role="switch" bind:checked={toggles.b} />
			Date Based Download
		</label>
		{#if toggles.b}
			<label for="date">Pick Date
				<input type="date" id="date" name="date" bind:value={selectedDate} />
			</label>
		{/if}
	</fieldset>

		<fieldset>
		<label for="end-date-switch">
			<input type="checkbox" id="end-date-switch" name="end-date-switch" role="switch" bind:checked={toggles.b} />
			Date Based Download
		</label>
		{#if toggles.b}
			<label for="date">Pick Date
				<input type="date" id="date" name="date" bind:value={selectedDate} />
			</label>
		{/if}
	</fieldset>

	<button type="submit">Submit</button>
</form>

{#if responseMessage}
	<p>{responseMessage}</p>
{/if}

<hr>

{#if downloadMessage}
	<p>{downloadMessage}</p>
{/if}

<hr>

{#if customMessage}
	<p>{customMessage}</p>
{/if}

<hr>

{#if errorMessage}
	<p>{errorMessage}</p>
{/if}
