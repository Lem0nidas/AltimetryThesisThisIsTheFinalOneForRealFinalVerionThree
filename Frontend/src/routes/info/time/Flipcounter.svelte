<script lang="ts">
	import { onMount } from 'svelte';

	let date1985: Date = new Date('1985-01-01T00:00:00Z');
	let unixTime1985: number = $state(0);

	const updateUnixTime = () => {
		unixTime1985 = Math.floor((Date.now() - date1985.getTime()) / 1000);
	};

	onMount(() => {
		const interval = setInterval(updateUnixTime, 1000);
		return () => clearInterval(interval);
	});

	const getTimeParts = (seconds: number) => {
		const years = Math.floor(seconds / 31_536_000);
		seconds %= 31_536_000;

		const days = Math.floor(seconds / 86_400);
		seconds %= 86_400;

		const hours = Math.floor(seconds / 3600);
		seconds %= 3600;

		const minutes = Math.floor(seconds / 60);
		const secs = seconds % 60;

		return { years, days, hours, minutes, secs };
	};

	let time = $derived(() => getTimeParts(unixTime1985));
	const digits = $derived(() => unixTime1985.toLocaleString().split(''));
</script>

<strong>Seconds since Jan 1, 1985:</strong><br />
<div class="digits">
	{#each digits() as d}
		<span class="counter">
			{d}
		</span>
	{/each}
</div>
<small>
	{time().years}y {time().days}d {time().hours}h
	{time().minutes}m {time().secs}s
</small>

<style>
	.digits {
		font-family: ui-monospace, monospace;
		font-size: 2.5rem;
		font-weight: 500;
		display: flex;
		gap: 0.15em;
	}
</style>
