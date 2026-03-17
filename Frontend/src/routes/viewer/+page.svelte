<script lang="ts">
	import type { NetcdfFile } from '$lib/types';
	import { ncDataStore } from '$lib/stores';
	import { fade } from 'svelte/transition';
	import { requestNetcdf } from '$lib';
	import { onDestroy, tick } from 'svelte';
	import Plotly from 'plotly.js-dist';
	import { X } from '@lucide/svelte';

	let name: string = $state('');
	let ncData: NetcdfFile = $state({});
	let dragCounter: number = $state(0);
	let isDragging: boolean = $state(false);
	let showMapPlot: boolean = $state(false);
	let showLinePlot: boolean = $state(false);
	let selectedVariable: string = $state('');
	let mapPlotDiv: HTMLDivElement | null = $state(null);
	let linePlotDiv: HTMLDivElement | null = $state(null);

	const unsubscribe = ncDataStore.subscribe((data) => {
		ncData = data;
	});
	onDestroy(() => {
		unsubscribe();
	});

	function handleVariableClick(item: string) {
		selectedVariable = item;
	}

	function handleDragEnter(e: DragEvent) {
		e.preventDefault();
		dragCounter++;
		isDragging = true;
	}

	function handleDragLeave(e: DragEvent) {
		e.preventDefault();
		dragCounter--;
		if (dragCounter == 0) {
			isDragging = false;
		}
	}

	function openExplorer() {
		document.getElementById('hiddenInput')?.click();
	}

	function handleCsvRequest(variable: string) {
		const variableObject = ncData[variable];
		const dimension = variableObject.dimension;
		const values = variableObject.values;
		const attributes = variableObject.attributes;

		let csvContent = '';
		csvContent += 'Attribute, Value\n';
		for (const [key, value] of Object.entries(attributes)) {
			csvContent += `${key},${value}\n`;
		}

		if (dimension.includes('time')) {
			csvContent += '\nIndex, Time, Value\n';
			values.forEach((val: number, index: number) => {
				const timeValue = ncData['time'].values[index];
				csvContent += `${index},${timeValue},${val}\n`;
			});
		} else {
			csvContent += '\nIndex,Value\n';
			values.forEach((val: number, index: number) => {
				csvContent += `${index},${val}\n`;
			});
		}
		
		const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });

		const url = URL.createObjectURL(blob);
		const link = document.createElement('a');

		link.href = url;
		link.download = `${name}_${variable}.csv`;
		document.body.appendChild(link);
		link.click();

		document.body.removeChild(link);
		URL.revokeObjectURL(url);
	}

	async function handleLinePlot(variable: string) {
		showLinePlot = true;
		await tick();

		const variableObject = ncData[variable];
		const xTime: string[] = ncData['time'].values.map((sec: number) => new Date(Date.UTC(1985, 0, 1) + sec *1000).toISOString());
		const yData: number[] = variableObject.values;
		const name: string = variableObject.attributes['long_name'];
		const units: string = variableObject.attributes['units'];
		const layout = {
			title: {text: `${name} (${units})`, font: { size: 20 }, x: 0.5},
			// xaxis: { title: 'Time', type: 'date', font: { size: 20 }},
			// yaxis: { title: `${name} (${units})`, font: { size: 20 }},
		};
		
		Plotly.newPlot(
			linePlotDiv, 
			[{
				x: xTime,
				y: yData,
				type: "scatter",
				mode: "lines+markers",

			}], 
			layout, 
			{ responsive: true },
		);
		setTimeout(() => Plotly.Plots.resize(linePlotDiv), 50);
	}

	async function handleMapPlot(variable: string) {
		showMapPlot = true;
		await tick();

		const variableObject = ncData[variable];
		const lat = ncData['lat'].values;
		const lon = ncData['lon'].values;
		const values = variableObject.values;
		const name: string = variableObject.attributes['long_name'];
		const units: string = variableObject.attributes['units'];

		const layout = {
			geo: {
				projection: { type: 'natural earth' },
				showland: true,
				landcolor: 'rgb(240, 240, 240)',
				subunitcolor: 'rgb(217, 217, 217)',
			},
			title: {text: `${name} (${units})`, font: { size: 20 }, x: 0.5},
		};

		Plotly.newPlot(
			mapPlotDiv,
			[{
				type: 'scattergeo',
				mode: 'markers',
				lat: lat,
				lon: lon,
				marker: {
					size: 12,
					color: values,
					colorscale: 'Bluered',
					cmin: Math.min(...values),
					cmax: Math.max(...values),
					colorbar: { title: `${name} values` }
				},
				text: values.map(v => `${v}`),
			}],
			layout,
			{ responsive: true },
		);
		setTimeout(() => Plotly.Plots.resize(mapPlotDiv), 50);
	}

	async function handleFileUpload(e: Event): Promise<void> {
		e.preventDefault();
		const uploadedFile = (e.target as HTMLInputElement).files?.[0];
		if (!uploadedFile) return;

		await handleFile(uploadedFile);
	}

	async function handleFileDrop(e: DragEvent): Promise<void> {
		e.preventDefault();
		const droppedFile = e.dataTransfer?.files[0];
		if (!droppedFile) return;

		await handleFile(droppedFile);
	}

	async function handleFile(file: File) {
		if (
			!(file.type in ['application/x-netcdf', 'application/netcdf'] || file.name.endsWith('.nc'))
		) {
			alert('Only .nc files allowed');
			return;
		}

		isDragging = false;
		selectedVariable = '';
		name = file.name;

		try {
			const data = await requestNetcdf(file);
			console.log('NetCDF data received:', data);
			console.log('Filename:', name);
		} catch (err) {
			console.error('Failed to load NetCDF:', err);
		}
	}
</script>

<svelte:window
	on:dragenter={handleDragEnter}
	on:dragover={(e) => e.preventDefault()}
	on:dragleave={handleDragLeave}
	on:drop={handleFileDrop}
/>

{#if ncData}
	<div class="container">
		<div class="left">
			<strong>"filename": {name}</strong>
			<br />
			<ul>
				{#each Object.entries(ncData) as [key, value]}
					<li>
						<button class="var-button" onclick={() => handleVariableClick(key)}>{key}</button>
					</li>
				{/each}
			</ul>
		</div>

		<div class="divider"></div>

		<div class="right">
			{#if selectedVariable}
				<strong>"{selectedVariable}":</strong>
				<ul>
					{#each Object.entries(ncData[selectedVariable].attributes) as [key, value]}
						<li>{key} = {value}</li>
					{/each}
				</ul>

				<div class="options">
					<button class="generator-button" onclick={() => handleCsvRequest(selectedVariable)}
						>Generate CSV data</button
					>
					<button class="line-plot-button" onclick={() => handleLinePlot(selectedVariable)}>Create line plot</button>
					<button class="map-plot-button" onclick={() => handleMapPlot(selectedVariable)}>Create map plot</button>
				</div>
			{/if}
		</div>
	</div>
{:else}
	<div class="wrapper">
		<div class="cover-group">
			<p>Drop or Select a file</p>
			<input
				id="hiddenInput"
				type="file"
				style="display: none;"
				accept=".nc"
				multiple={false}
				onchange={handleFileUpload}
			/>
			<button class="upload-button" onclick={() => openExplorer()}>Browse ...</button>
		</div>
	</div>
{/if}

{#if isDragging}
	<div class="drop-overlay" transition:fade={{ duration: 300 }}>
		<p>Drop NetCDF file</p>
	</div>
{/if}

{#if showLinePlot}
	<div class="line-plot-overlay" transition:fade={{ duration: 300 }}>
		<div class="line-plot-container">
			<button class="close-btn" onclick={() => showLinePlot = false}>
				<X size={20} />
			</button>

			<div class="line-plot" bind:this={linePlotDiv}></div>
		</div>
	</div>
{/if}

{#if showMapPlot}
	<div class="map-plot-overlay" transition:fade={{ duration: 300 }}>
		<div class="map-plot-container">
			<button class="close-btn" onclick={() => showMapPlot = false}>
				<X size={20} />
			</button>

			<div class="map-plot" bind:this={mapPlotDiv}></div>
		</div>
	</div>
{/if}

<style>
	.var-button {
		all: unset;
		cursor: pointer;
	}

	.container {
		display: flex;
		height: calc(105vh - var(--page-padding-top));
	}

	.wrapper {
		height: calc(100vh - var(--page-padding-top));
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.cover-group {
		text-align: center;
	}

	.left,
	.right {
		flex: 1;
		padding: 1rem;
		overflow-x: auto;
		flex-direction: column;
	}

	.divider {
		width: 1px;
		background: #ccc;
	}

	.options {
		margin-top: auto;
		display: flex;
		justify-content: space-evenly;
		padding-top: 1rem;
	}

	.drop-overlay {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.6);
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 2rem;
		z-index: 9999;
		pointer-events: all;
	}

	.line-plot-overlay,
	.map-plot-overlay {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.6);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
	}

	.line-plot-container,
	.map-plot-container {
		background: white;
		width: 90%;
		height: 80%;
		border-radius: 8px;
		padding: 1rem;
		position: relative;
	}

	.line-plot,
	.map-plot {
		width: 100%;
		height: 100%;
	}

	.close-btn {
		position: absolute;
		top: 10px;
		z-index: 2000;
	}
</style>
