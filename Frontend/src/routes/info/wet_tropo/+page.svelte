<h1>Wet tropospheric correction</h1>

<p>
	The wet tropospheric correction (the negative of zenith wet delay, ZWD) accounts for the delay of
	the radar signal in the atmosphere due to the presence of water vapour. This effect is non-
	dispersive, i.e., it is the same on Ku-, S- and C-band frequencies, and it can be determined by
	integrating a function of water vapour density and temperature [e.g., Askne and Nordius, 1987],
	which to good approximation simplifies to ZWD = IWVR w (k 3 /Tm + k 2′ ) where IWV is integrated
	water vapour, Tm is the mean temperature in the atmospheric column, and R w , k 2′ and k 3 are
	constants [Bevis et al., 1994]. The mean temperature can further be approximated from model data
	of near-surface air temperature, Ts , by Tm = 50.4 + 0.789Ts [Mendes et al., 2000]. In this way,
	the 6-hourly models of integrated water vapour and near- surface temperature are interpolated in
	space and time and then converted to a wet tropo- spheric correction. Generally, the temporal
	spacing of the model grids is 6 hours, but since the power of the water vapour content at 12 and
	24 hours is low, an air tide correction like in case of the pressure is not needed.
</p>
