<script lang="ts">
	import Nav from './Nav.svelte';

	let { children } = $props();
</script>

<Nav />

{@render children()}

<style>
	:global(body, h1, h2, h3, p) {
		font-family: 'Cormorant Garamond', serif;
	}

	:root {
		--sidebar-width: 13rem;
		--page-padding-side: 4.8rem;
		--page-padding-top: 6rem;
		--page-padding-bottom: 6rem;
	}
</style>
