
<script lang="ts">
	import Menu from '/home/leon/node_modules/@lucide/svelte/dist/icons/menu';
	import Home from '/home/leon/node_modules/@lucide/svelte/dist/icons/home';
	import Download from '/home/leon/node_modules/@lucide/svelte/dist/icons/download';
	import View from '/home/leon/node_modules/@lucide/svelte/dist/icons/view';
	import Info from '/home/leon/node_modules/@lucide/svelte/dist/icons/info';
	import BookText from '/home/leon/node_modules/@lucide/svelte/dist/icons/book-text';
	import CircleHelp from '/home/leon/node_modules/@lucide/svelte/dist/icons/circle-help';
	import Mail from '/home/leon/node_modules/@lucide/svelte/dist/icons/mail';


	let menuOpen = false;

	function toggleMenu() {
		menuOpen = !menuOpen;
	}

    function closeMenu() {
        menuOpen = false;
    }
</script>

<style>
	nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 5px;
		background-color: #1a1a1a;
		color: white;
		position: relative;
	}

	.title {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		font-size: 1.25rem;
		font-weight: bold;
        color: var(--primary);
	}

	.menu-btn {
		background: none;
		border: none;
		font-size: 0rem;
		color: white;
		cursor: pointer;
	}

    .dropdown {
		position: absolute;
		top: 100%;
		left: 0;
		background-color: #2b2b2b;
		border: 1px solid var(--muted-border-color);
		border-radius: var(--border-radius);
		box-shadow: var(--box-shadow);
		padding: 0.75rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		z-index: 100;
	}

	.dropdown a {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem;
		color: white;
		text-decoration: none;
	}

	.dropdown a:hover {
		color: #ddd;
	}
</style>

<nav>
	<!-- Hamburger Menu -->
	<button class="menu-btn" on:click={toggleMenu}><Menu /></button>

	<!-- Center Title -->
	<div class="title">Altimetry Portal</div>

	<!-- Dropdown Menu -->
	{#if menuOpen}
		<div class="dropdown">
			<a href="/" on:click={closeMenu}><Home /> Home</a>
			<a href="/download" on:click={closeMenu}><Download /> <span>Download</span></a>
			<a href="/viewer" on:click={closeMenu}><View /> <span>NetCDF Viewer</span></a>
			<a href="/info" on:click={closeMenu}><Info /> <span>More Info</span></a>
			<a href="/about" on:click={closeMenu}><BookText /> <span>About</span></a>
			<a href="/help" on:click={closeMenu}><CircleHelp /> <span>Help</span></a>
			<a href="/contact" on:click={closeMenu}><Mail /> <span>Contact</span></a>
		</div>
	{/if}
</nav>
