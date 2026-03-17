<script lang="ts">
	let { selectedProperty = $bindable(), type, disable } = $props();
	let toggle = $state(false);

	$effect(() => {
		if (!toggle) {
			selectedProperty = '';
		}
	});
</script>

<fieldset disabled={disable}>
	<label for={`${type}-switch`}>
		<input type="checkbox" name="type-switch" role="switch" bind:checked={toggle} />
		Pick Specific {type}
	</label>
	{#if toggle}
		<label for="type">{type} number:</label>
		<input
			type="text"
			id="type"
			placeholder="e.g. 0234"
			maxlength={type === 'Pass' ? 4 : 3}
			bind:value={selectedProperty}
			onblur={() => {
				if (type === 'Pass' && selectedProperty?.trim()) {
					selectedProperty = selectedProperty.padStart(4, '0');
				} else if (type === 'Cycle' && selectedProperty?.trim()) {
					selectedProperty = selectedProperty.padStart(3, '0');
				}
			}}
		/>
	{/if}
</fieldset>
