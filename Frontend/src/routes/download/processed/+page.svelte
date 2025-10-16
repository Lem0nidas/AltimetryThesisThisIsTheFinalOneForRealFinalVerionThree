<script lang="ts">
	import { X } from '@lucide/svelte';
	import type { RADSVariable } from '$lib/data/variables';
	import type { RADSSatellite } from '$lib/data/satellites';
	import { variables } from '$lib/data/variables';
	import { satellites } from '$lib/data/satellites';
	import { processedDownload } from '$lib';
	import Map from '$lib/components/Map.svelte';
	import Switch from '$lib/components/Switch.svelte';

	let { children } = $props();

	let selectedSatellite: RADSSatellite = $state({ name: '', code: '' });
	let selectedVariable: RADSVariable | null = $state(null);
	let selectedCycle: string = $state('');
	let listBoxItems: RADSVariable[] = $state([]);
	let options: Record<string, string> = $derived.by(() => {
		let opts: Record<string, string> = {
			vars: listBoxItems.map((v) => v.varName).join(',')
		};

		if (selectedCycle !== '') {
			opts.cycle = selectedCycle;
		}

		return opts;
	});

	let toggles = $state({
		file_type: false
	});

	let messages = $state({
		response: '',
		error: '',
		download: '',
		custom: '',
		date: ''
	});

	function addToList() {
		if (selectedVariable && !listBoxItems.some((item) => item.name === selectedVariable?.name)) {
			listBoxItems = [...listBoxItems, selectedVariable];
		}
	}

	function removeFromList(index: number) {
		listBoxItems = listBoxItems.filter((_, i) => i !== index);
	}

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		if (!selectedSatellite) {
			messages.response = 'Please select a satellite';
		} else if (listBoxItems.length == 0) {
			messages.response = 'Please select a variable'; //TODO Don't execute code
		}

		try {
			messages.response = await processedDownload(selectedSatellite.code, options);
		} catch (err) {
			(messages.error = 'Error contacting server.'), console.log(err);
		}
	}
</script>

<h1>Welcome to Download Processed Data page</h1>

<form onsubmit={handleSubmit}>
	<fieldset>
		<label for="satellite">Choose a satellite</label>
		<select id="satellite" bind:value={selectedSatellite} required>
			<option value="" disabled selected>Select one</option>
			{#each satellites as sat}
				<option value={sat}>{sat.name}</option>
			{/each}
		</select>
	</fieldset>

	<Switch bind:selectedProperty={selectedCycle} type="Cycle" />

	<fieldset>
		<label for="listbox">Selected Items:</label>
		<div class="listbox-wrapper">
			<ul id="listbox">
				{#each listBoxItems as items, index}
					<li>
						<span>{items.name}</span>
						<button
							id="removeButton"
							onclick={() => removeFromList(index)}
							aria-label="Remove item"
						>
							<X size={16} />
						</button>
					</li>
				{/each}
			</ul>
		</div>

		<label for="variables">Pick variables to calculate</label>
		<select name="variables" id="variables" bind:value={selectedVariable} required>
			<option value={null} disabled selected>Select any amount</option>
			{#each variables as variable (variable.varName)}
				<option value={variable} onclick={addToList}>{variable.name}</option>
			{/each}
		</select>
	</fieldset>

	<fieldset id="button">
		<button type="submit">Submit</button>
		<label for="file-type-switch">
			NetCDF File
			<input id="file-type-switch" type="checkbox" role="switch" bind:checked={toggles.file_type} />
			ASCII File
		</label>
	</fieldset>
</form>

<Map />

{@render children?.()}

<style>
	:root {
		--switch-color: #fd0dd5; /* active color */
		--switch-background-color: #adb5bd; /* inactive background */
	}
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
		margin-bottom: 1rem;
	}

	fieldset#button {
		display: grid;
		justify-content: center;
	}

	ul#listbox {
		display: flex;
		flex-wrap: wrap;
		gap: 0.2em;
		max-height: 250px;
		overflow-y: auto;
		list-style: none;
		padding: 0;
		margin: 0.2rem;
	}

	ul#listbox li {
		display: flex;
		align-items: center;
		padding: 0.3rem 0.6rem;
		border: 1px solid #eee;
		border-radius: 25px;
		font-size: medium;
		width: fit-content;
	}

	ul#listbox li:hover {
		background-color: #ffffff0a;
		box-shadow: 0 0 5px rgba(0, 0, 0, 0.4);
		cursor: default;
	}

	button#removeButton {
		font-size: 1rem;
		line-height: 1;
		padding: 0;
		margin-left: 0.5rem;
		background: none;
		border: none;
		color: rgb(17, 17, 17);
		cursor: pointer;
		transition: transform 0.3s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	button#removeButton:hover {
		transform: rotate(90deg);
		color: red;
	}

	label[for='file-type-switch'] {
		margin: auto 50px;
	}

	/* TODO Fix the colors */
	input#file-type-switch {
		margin-left: 0.5rem;
		--pico-background-color: #14c814;
		--pico-border-color: #146414;
		--pico-form-element-focus-color: #66aacc;
	}

	input#file-type-switch:checked {
		--pico-background-color: #14cc8e;
		--pico-border-color: #14cc32;
	}

	.listbox-wrapper {
		height: 270px;
		border: 1px solid #2a3140;
		border-radius: 20px;
		background-color: #1c212c;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
		margin-bottom: 1rem;
	}
</style>
