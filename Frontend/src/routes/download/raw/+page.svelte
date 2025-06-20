<script lang="ts">
	import {
		requestCustomDownload,
		requestDownload,
		requestLatestDownload,
		requestDateDownload
	} from "$lib/api/rads";
	import { Satellite } from "@lucide/svelte";

	let selectedSatellite = $state('');
	let selectedCycle = $state('');
	let selectedPass = $state('');
	let selectedStartDate = $state('');
	let selectedEndDate = $state('');

	let toggles = $state({
		pass: false,
		startDate: false,
		endDate: false,
	});
	
	let messages = $state({
		response: '',
		error: '',
		download: '',
		custom: '',
		date: '',
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
			messages.response = 'Please select a satellite.';
			return;
		}

		try {
			messages.response = await requestDownload(selectedSatellite);
			messages.download = await requestLatestDownload(selectedSatellite);
			messages.custom = await requestCustomDownload(selectedSatellite, selectedCycle, selectedPass);
			
			if (toggles.startDate && selectedStartDate) {
				messages.date = await requestDateDownload(
					selectedSatellite,
					selectedStartDate,
					toggles.endDate ? selectedEndDate : ''
				);
			}
		} catch (err) {
			messages.error = 'Error contacting server.';
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
			<input type="checkbox" name="pass-switch" role="switch" bind:checked={toggles.pass} />
			Pick Specific Pass
		</label>
		{#if toggles.pass}
			<label for="pass">Pass number:</label>
			<input type="text" id="pass" bind:value={selectedPass} placeholder="e.g. 0234" />
		{/if}
	</fieldset>

	<fieldset>
		<label for="start-date-switch">
			<input type="checkbox" name="start-date-switch" role="switch" bind:checked={toggles.startDate} />
			Date Based Download
		</label>
		{#if toggles.startDate}
			<label for="start-date">Pick Start Date:</label>
			<input type="date" name="start-date" bind:value={selectedStartDate} />

			<label for="end-date-switch">
				<input type="checkbox" name="end-date-switch" role="switch" bind:checked={toggles.endDate} />
				Include End Date
			</label>

			{#if toggles.endDate}
				<label for="end-date">Pick End Date:</label>
				<input type="date" name="end-date" bind:value={selectedEndDate} />
			{/if}
		{/if}
	</fieldset>

	<button type="submit">Submit</button>
</form>

{#each Object.entries(messages) as [key, value]}
	{#if value}
		<hr />
		<p>{value}</p>
	{/if}
{/each}


<style>
	/* Wrapper to center everything */
	form {
		max-width: 600px;
		margin: 2rem auto;
		padding: 2rem;
		border-radius: 10px;
		background-color: #1c1f26;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
	}

	h1 {
		text-align: center;
		margin-top: 1.5rem;
		color: white;
	}

	fieldset {
		border: none;
		margin-bottom: 1.5rem;
	}

	label {
		display: block;
		margin-bottom: 0.5rem;
		color: #ccc;
		font-weight: 500;
	}

	input[type="text"],
	input[type="date"],
	select {
		width: 100%;
		padding: 0.5rem;
		border-radius: 5px;
		border: 1px solid #444;
		background-color: #1f1f1f;
		color: white;
	}

	input[type="checkbox"] {
		margin-right: 0.5rem;
	}

	button {
		width: 100%;
		padding: 0.75rem;
		background-color: #007baf;
		color: white;
		font-weight: bold;
		border: none;
		border-radius: 5px;
		cursor: pointer;
	}

	button:hover {
		background-color: #006799;
	}

	p {
		text-align: center;
		color: #ddd;
	}
</style>
