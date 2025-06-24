
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
	let fadingOut = false;

	function toggleMenu() {
		if (menuOpen) {
			fadingOut = true;
			setTimeout(() => {
				menuOpen = false;
				fadingOut = false;
			}, 500);
		} else {
			menuOpen = true;
		}
	}

	function closeMenu() {
		fadingOut = true;
		setTimeout(() => {
			menuOpen = false;
			fadingOut = false;
		}, 500);
	}
</script>


<nav>
	<!-- Hamburger Menu -->
	<button class="menu-btn" on:click={toggleMenu}><Menu /></button>

	<!-- Center Title -->
	<div class="title">Altimetry Portal</div>

	<!-- Dropdown Menu -->
	{#if menuOpen}
		<div class="dropdown" class:open={menuOpen} class:fade-out={fadingOut}>
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


<style>
	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	@keyframes fadeOut {
		from { opacity: 1; }
		to { opacity: 0; }
	}

	nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.75rem 1.5rem;
		background-color: #1a1a1a;
		color: white;
		border-radius: 0 0 12px 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
		position: relative;
		transition: background-color 0.3s ease;
	}

	.title {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		font-size: 1.25rem;
		font-weight: bold;
        color: var(--primary,);
		white-space: nowrap;
	}

	.menu-btn {
		background: none;
		border: none;
		font-size: 0rem;
		color: white;
		cursor: pointer;
		transition: color 0.2s ease;
	}

	.menu-btn:hover {
		color: #ccc
	}

	.dropdown {
		position: absolute;
		top: 100%;
		left: 0;
		margin-top: 0.5rem;
		background-color: #2b2b2b;
		border-radius: 10px;
		border: 1px solid var(--muted-border-color, #444);
		box-shadow: 0 0 12px rgba(0, 0, 0, 0.6);
		padding: 0.75rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		z-index: 100;
		animation: fadeIn 0.5s ease-in-out forwards;
	}

	.dropdown.fade-out {
		animation: fadeOut 0.5s ease-in-out forwards;
	}

	.dropdown a {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 0.75rem;
		color: white;
		text-decoration: none;
		border-radius: 8px;
		transition: background-color 0.2s ease, box-shadow 0.2s ease;
	}

	.dropdown a:hover {
		background-color: #383838;
		box-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
		color: #f0f0f0;
	}
</style>