<h1>Wet tropospheric correction</h1>

<p>
	The wet tropospheric correction (the negative of zenith wet delay, ZWD) accounts for the delay of
	the radar signal in the atmosphere due to the presence of water vapour. This effect is non-
	dispersive, i.e., it is the same on Ku-, S- and C-band frequencies, and it can be determined by
	integrating a function of water vapour density and temperature [e.g., Askne and Nordius, 1987],
	which to good approximation simplifies to
</p>
<br />
<math class="a" xmlns="http://www.w3.org/TR/MathML/">
	<mi>ZWD</mi>
	<mo>=</mo>
	<mi>IWV</mi>
	<mo>*</mo>
	<msub>
		<mi>R</mi>
		<mi>w</mi>
	</msub>
	<mo>* (</mo>
	<mfrac>
		<msub>
			<mi>k</mi>
			<mn>3</mn>
		</msub>
		<msub>
			<mi>T</mi>
			<mi>m</mi>
		</msub>
	</mfrac>
	<mo>+</mo>
	<msub>
		<mi>k</mi>
		<mi>2</mi>
	</msub>
	<mo>'</mo>
	<mo>)</mo>
</math>
<br />
<p>
	where IWV is integrated water vapour, T<sub>m</sub> is the mean temperature in the atmospheric
	column, and R<sub>w</sub> , k'<sub>2</sub> and k<sub>3</sub> are constants [Bevis et al., 1994].
	The mean temperature can further be approximated from model data of near-surface air temperature,
	T<sub>s</sub> , by [Mendes et al., 2000].
</p>
<br />
<math class="b" xmlns="http://www.w3.org/TR/MathML/">
	T<sub>m</sub> = 50.4 + 0.789 * T<sub>s</sub>
</math>
<br />
<p>
	In this way, the 6-hourly models of integrated water vapour and near- surface temperature are
	interpolated in space and time and then converted to a wet tropospheric correction. Generally, the
	temporal spacing of the model grids is 6 hours, but since the power of the water vapour content at
	12 and 24 hours is low, an air tide correction like in case of the pressure is not needed.
</p>

<style>
	math.a {
		font-style: italic;
		display: block;
		padding-left: 45vh;
	}

	math.b {
		font-style: italic;
		display: block;
		padding-left: 50vh;
	}
</style>
