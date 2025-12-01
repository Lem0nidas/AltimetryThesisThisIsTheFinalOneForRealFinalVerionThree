<script lang="ts">
	import Nav from './Nav.svelte';

	let { children } = $props();
</script>

<div class="layout-wrapper">
	<Nav />
</div>

{@render children()}

<style>
</style>
