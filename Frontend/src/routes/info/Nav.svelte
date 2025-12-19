<nav class="docs" aria-label="Docs">
	<ul class="sidebar">
		<li class="group">
			<h3>Introduction</h3>
			<ul>
				<li><a class="page" href="/info/overview">Overview</a></li>
			</ul>
		</li>
		<li class="group">
			<h3>Time and location</h3>
			<ul>
				<li><a class="page" href="/info/time">Time</a></li>
				<li><a class="page" href="/info/lat_lon">Latitude & longitude</a></li>
				<li><a class="page" href="/info/altitude">Orbital altitude</a></li>
			</ul>
		</li>
		<li class="group">
			<h3>Sea level variables</h3>
			<ul>
				<li><a class="page" href="/info/sla">Sea level anomaly</a></li>
				<li><a class="page" href="/info/altimeter_range">Altimeter range</a></li>
				<li><a class="page" href="/info/altimeter_range_RMS">Altimeter range RMS</a></li>
				<li><a class="page" href="/info/dry_tropo">Dry tropospheric correction</a></li>
				<li><a class="page" href="/info/wet_tropo">Wet tropospheric correction</a></li>
				<li><a class="page" href="/info/iono_corr">Ioonospheric correction</a></li>
				<li><a class="page" href="/info/atmo_corr">Atmospheric correction</a></li>
				<li><a class="page" href="/info/solid_tide">Solid earth tide</a></li>
				<li><a class="page" href="/info/pole_tide">Pole tide</a></li>
				<li><a class="page" href="/info/ocean_tide">Ocean & Load tide</a></li>
				<li><a class="page" href="/info/internal_tide">Internal tide</a></li>
				<li><a class="page" href="/info/ssbias">Sea state bias</a></li>
				<li><a class="page" href="/info/mean_sea_surf">Mean sea surface</a></li>
				<li><a class="page" href="/info/geoid">Geoid</a></li>
			</ul>
		</li>
		<li class="group">
			<h3>Wind speed and wave height variables</h3>
			<ul>
				<li><a class="page" href="/info/swh">Significant wave height</a></li>
				<li><a class="page" href="/info/wind_speed">Wind speed</a></li>
			</ul>
		</li>
		<li class="group">
			<h3>Variables for data editing</h3>
			<ul>
				<li><a class="page" href="/info/bath_topo">Bathymetry & Topography</a></li>
			</ul>
		</li>
	</ul>
</nav>

<style>
	nav {
		position: fixed;
		top: auto;
		left: 0;
		width: var(--sidebar-width);
		height: 100vh;
		padding-bottom: 10vh;
		overflow-y: auto;
		font-size: large;
		background: hsl(220, 8%, 10%);
	}

	nav ul {
		display: block;
		position: relative;
		overflow-x: hidden;
		overflow-y: auto;

		color: hsl(220, 3%, 80%);
	}

	nav li {
		padding: 0 0.5rem 0 0;
	}

	.sidebar {
		padding-left: 2rem;
		padding-top: 3rem;
		margin: 0 0 0 auto;
	}

	li.group {
		margin: 0 0 4rem;
		display: block;
	}

	li ul {
		margin: 0;
	}

	li a {
		margin: 0;
		padding-right: 0.5rem;
		display: block;
		position: relative;
		text-decoration: none;
		color: aliceblue;
	}

	h3 {
		margin: 0 0 0.3rem;
		text-decoration: underline;
		font-size: larger;
	}
</style>
