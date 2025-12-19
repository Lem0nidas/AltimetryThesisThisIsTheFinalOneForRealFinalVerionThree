<h1>Ocean & Load tide</h1>

<p>
	The (pure) ocean tide is the variation of the height of the water column as a result of luni-solar
	attraction. Since this is measured relative to a fixed point on the solid earth (like the sea
	floor), the ocean tide compares directly to tide gauge measurements. The load tide is the effect
	of the tides weighing on the elastic earth. In general, when the ocean tide goes up, the sea floor
	is going down, hence reducing the sum of the two, the geocentric ocean tide. Consequently, in
	order to detide the measurement of the water surface from altimetry, both the ocean tide and the
	load tide need to be subtracted over ocean surfaces, while over lakes only the load tide is
	subtracted. Although some altimeter products provide the geocentric ocean tide, we have chosen to
	keep ocean and load tide separate, for two reasons:
</p>
<ol>
	<li>it makes it easier to differentiate tides over land/lakes and ocean</li>
	<li>
		it makes it easier to add regional tides which are generally expressed as pure ocean tides
	</li>
</ol>

<p>
	Tides are expressed as the sum of a (large) number of waves with different frequencies, each
	combinations of the frequencies associated with the rotation and progression of the earth, sun and
	moon. A select portion of those waves are expressed as grids of amplitude and phase, which can be
	interpolated in space and evaluated at the time of the altimeter measurement. Then, by a process
	called admittance, the amplitude and phase of a number of minor tides are inferred.
	<br />
	<br />
	Tide models generally only include the diurnal and semi-diurnal waves (those around a period of 12
	and 24 hours). On top of that there are secondary and tertiary waves with periods of a week or longer.
	Most of these waves can be expressed by a simple latitude and time dependent equilibrium model (the
	long-period equilibrium tide). The FES ocean tide models also include the non-equilibrium component
	of the monthly, fortnightly, tri-monthly, and weekly tides.
	<br />
	<br />
	Although the FES and GOT models are global, they are limited in scope. Over land, the ocean tide is
	not defined and will be set to the NaN value. In some coastal regions, where the models may likely
	not be defined, the ocean tide value is set to NaN as well.
</p>
