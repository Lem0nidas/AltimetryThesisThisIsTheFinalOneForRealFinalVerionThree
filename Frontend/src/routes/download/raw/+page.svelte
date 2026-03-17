<script lang="ts">
	import { requestCustomDownload, requestDateDownload } from '$lib';
	import Switch from '$lib/components/Switch.svelte';
	import type { RADSSatellite } from '$lib/data/satellites';
	import { satellites } from '$lib/data/satellites';

	let selectedSatellite: RADSSatellite = $state({ name: '', code: '', start: '', end: '' });
	let selectedCycle = $state('');
	let selectedPass = $state('');
	let currentDate = new Date().toISOString().split('T')[0];
	let selectedStartDate = $state('');
	let selectedEndDate = $state('');

	let toggles = $state({
		pass: false,
		dateSwitch: true,
		startDate: false
	});

	let messages = $state({
		response: '',
		error: '',
		download: '',
		custom: '',
		date: ''
	});

	$effect(() => {
		if (selectedSatellite.name != '') {
			toggles.dateSwitch = false;
			selectedEndDate = (selectedSatellite.end !== 'present') ? selectedSatellite.end : currentDate;;
		}

		if (!toggles.pass) {
			selectedPass = '';
		}

		if (toggles.startDate) {
			selectedCycle = '';
			selectedPass = '';
		}
	});

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		if (!selectedSatellite) {
			messages.response = 'Please select a satellite.';
			return;
		}

		try {
			if (!toggles.startDate && selectedCycle) {
				messages.response = await requestCustomDownload(
					selectedSatellite.code,
					selectedCycle,
					selectedPass
				);
			}

			if (toggles.startDate && selectedStartDate) {
				messages.date = await requestDateDownload(
					selectedSatellite.code,
					selectedStartDate,
					selectedEndDate
				);
			}
		} catch (err) {
			messages.error = 'Error contacting server.';
			console.error(err);
		}
	}
</script>

<h1>Download Raw Data page</h1>

<form onsubmit={handleSubmit}>
	<fieldset>
		<label for="satellite">Choose a satellite:</label>
		<select id="satellite" bind:value={selectedSatellite} required>
			<option value="" disabled selected>Select one</option>
			{#each satellites as sat}
				<option value={sat}>{sat.name}</option>
			{/each}
		</select>
	</fieldset>

	<fieldset disabled={toggles.startDate}>
		<label for="cycle">Type the cycle number:</label>
		<input
			type="text"
			id="cycle"
			placeholder="e.g. 015"
			maxlength="3"
			bind:value={selectedCycle}
			onblur={() => {
				if (selectedCycle?.trim()) {
					selectedCycle = selectedCycle.padStart(3, '0');
				}
			}}
		/>
	</fieldset>

	<Switch bind:selectedProperty={selectedPass} type="Pass" disable={toggles.startDate} />

	<fieldset disabled={toggles.dateSwitch}>
		<label for="start-date-switch">
			<input
				type="checkbox"
				name="start-date-switch"
				role="switch"
				bind:checked={toggles.startDate}
			/>
			Date Based Download
		</label>
		{#if toggles.startDate}
			<label for="start-date">Pick Date:</label>
			<div class="date-container">
				<input 
					type="date" 
					name="start-date" 
					min={selectedSatellite.start} 
					max={selectedSatellite.end} 
					bind:value={selectedStartDate} 
				/>
				<input 
					type="date" 
					name="end-date" 
					min={selectedSatellite.start} 
					max={selectedSatellite.end} 
					bind:value={selectedEndDate} 
				/>
			</div>
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

	input[type='text'],
	select {
		width: 100%;
		padding: 0.5rem;
		border-radius: 5px;
		border: 1px solid #444;
		background-color: #1f1f1f;
		color: white;
	}

	.date-container {
		display: flex;
		gap: 10%;
		justify-content: center;
	}

	input[type='date'] {
		width: 40%;
	}

	input[type='checkbox'] {
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
