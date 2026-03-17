<script lang="ts">
	import Flipcounter from './Flipcounter.svelte';

	let { children } = $props();
</script>

<h1>Time</h1>

<p>
	Time in the RADS data sets is stored as 8-byte floats in UTC seconds <a
		href="https://en.wikipedia.org/wiki/Epoch_(computing)"
		target="_blank"
		rel="noopener noreferrer"
		class="link">since 1 January 1985</a
	> . RADS will automatically convert these values into a few common time scales, depending on which
	time variable is selected. However, irrespective of the time scale, the clock references to UTC, rather
	than an atomic clock, meaning that leap seconds may result in a duplication of measurement times. No
	provision has been made to avoid confusion between measurements made before and after a leap second.
	The time corresponds to the moment of reflection of the radar pulse on the sea surface and is corrected
	for time tag biases.
</p>
<hr />
<div class="flip">
	<Flipcounter />
</div>

{@render children?.()}

<style>
	.flip {
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column;
		animation: fadeIn 3s forwards;
		opacity: 0;
	}

	@keyframes fadeIn {
		50% {
			opacity: 0;
		}
		100% {
			opacity: 1;
		}
	}

	.link {
		color: #1e90ff;
		text-decoration: none;
		transition: color 0.3s;
	}

	.link:hover {
		color: #ff4500;
	}
</style>
