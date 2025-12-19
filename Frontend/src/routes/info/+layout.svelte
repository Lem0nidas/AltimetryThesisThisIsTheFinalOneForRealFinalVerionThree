<script lang="ts">
	import Nav from './Nav.svelte';

	let { children } = $props();
</script>

<div class="layout-wrapper">
	<Nav />
	<div class="content">
		{@render children()}
	</div>
</div>

<style>
	/* .layout-wrapper {
		display: flex;
		flex-direction: column;
	} */

	.content {
		padding-left: calc(var(--sidebar-width) + var(--page-padding-side));
		padding-top: var(--page-padding-top);
		padding-bottom: var(--page-padding-bottom);
		padding-right: var(--page-padding-side);
	}
</style>
