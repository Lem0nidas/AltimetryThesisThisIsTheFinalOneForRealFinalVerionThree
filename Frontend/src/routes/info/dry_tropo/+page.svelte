<h1>Dry tropospheric correction</h1>

<p>
	The dry tropospheric correction (the negative of the zenith hydrostatic delay, ZHD) accounts for
	the delay of the radar signal in the atmosphere, not counting the effect of water vapour. This
	effect is non-dispersive, i.e., it is the same on all frequencies, and is proportional to the
	surface pressure [Saastamoinen, 1972]. The surface pressure, in turn, is determined by
	interpolation (in space and time) of model grids of surface (or sea level) pressure. Most
	altimeter missions provide the ECMWF operational analysis models as baseline.
	<br />
	<br />
	Generally, the temporal spacing of the model grids is 6 hours, while the spatial resolution varies.
	The 6-hourly interval between successive model grids hampers the capturing of 12- hourly and 24-hourly
	phenomena. Common 24-hourly traveling waves turn into standing waves, while 12-hourly variations are
	insufficiently described. These phenomena are consid- ered S1 and S2 air tides [Ponte and Ray, 2002].
	<br />
	<br />
	To remedy this problem an air tide correction is applied to the sea level pressure, by removing the
	air tide from the 6-hourly grids before spatio-temporal interpolation and then adding the air tide
	back for the time and location of the measurement. This correction is already applied to the ECMWF
	dry tropospheric correction on the Jason-2 GDRs; for all others it is corrected in the RADS processing.
</p>
