<script lang="ts">
	import { requestNetcdf } from '$lib';

	let file: {
		name: string;
		type: string;
	} | null = null;

	function hadleFileDrop(e: DragEvent) {
		e.preventDefault();
		const droppedFile = e.dataTransfer?.files[0];
		console.log('Droped file is : ' + droppedFile?.name);
		if (droppedFile) {
			file = {
				name: droppedFile.name,
				type: droppedFile.type
			};
			requestNetcdf(droppedFile);
		}
	}
</script>

<div role="region" class="zone" ondragover={(e) => e.preventDefault()} ondrop={hadleFileDrop}>
	{#if !file}
		<p>Drop files here</p>
	{:else}
		<img src="/file.png" alt="file icon" style="width:80px;" />
		<p>{file.name}</p>
	{/if}
</div>

<style>
	.zone {
		width: 300px;
		height: 120px;
		border: 2px dashed #aaa;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
