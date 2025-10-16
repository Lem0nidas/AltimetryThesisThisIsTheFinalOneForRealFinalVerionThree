<script lang="ts">
	let { selectedProperty = $bindable(), type } = $props();
	let toggle = $state(false);

	$effect(() => {
		if (!toggle) {
			selectedProperty = '';
		}
	});
</script>

<fieldset>
	<label for="{type}-switch">
		<input type="checkbox" name="type-switch" role="switch" bind:checked={toggle} />
		Pick Specific {type}
	</label>
	{#if toggle}
		<label for="type">{type} number:</label>
		<input type="text" id="type" placeholder="e.g. 0234" bind:value={selectedProperty} />
	{/if}
</fieldset>
