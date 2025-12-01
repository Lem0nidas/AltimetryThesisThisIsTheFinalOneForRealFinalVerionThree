<h1>Sea level anomaly</h1>

<p>
	The sea level anomaly (SLA) or sea surface height anomaly (SSHA) is the height for the sea surface
	relative to a long term mean. It can be constructed by subtracting from the satellite orbital
	altitude the altimeter range, propagation corrections, sea state bias, tides, and a mean sea
	surface model. The sea level anomaly in RADS is always computed on-the-fly. This means that the
	RADS soft- ware will gather the required variables and their selected flavours from the netCDF
	data files, edit those data based on the user-selected criteria, and then constructs the sea level
	anomaly based on those. If any of the variables that make up the sea level anomaly is not
	available, marked invalid, or is out of range, then the sea level anomaly is also marked invalid
	(set to the NaN value). In addition, variables that do not strictly make up the sea level anomaly
	(like wave height or wind speed) can be used as edit criteria, e.g. rejecting data with high sea
	states.
</p>
