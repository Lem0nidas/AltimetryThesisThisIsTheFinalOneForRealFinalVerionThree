<h1>Sea state bias</h1>

<p>
	Sea state bias (SSB) is the term used for any altimetric range offset as a function of the sea
	state (wave height, wind speed, wave age, swell). In fact, there are three components to the sea
	state bias: Electromagnetic (EM) bias is the tendency of a radar to measure towards the wave
	troughs since they are better reflectors than the wave peaks. Skewness bias comes from the fact
	that the sea surface has a skewed height distribution. While the altimeter measures the median
	height of the surface in the footprint, what we want to measure is the mean height, which is
	lower. Tracker bias is the any error in the waveform tracker that is a function of the sea state,
	which may be either instrumental or algorithmic. Because of the instrumental part of sea state
	bias, every altimeter, in principle, requires a dif- ferent sea state bias correction model. But
	also when a new tracker algorithm is implemented, the sea state bias changes. This is one of the
	reasons for the wide proliferation of SSB models. In the earlier days of altimetry the sea state
	bias was generally considered as a simple fraction, around –3.5%, of significant wave height
	[Chelton, 1994]. Then Gaspar et al. [1994] brought a major improvement in SSB modelling by
	expressing SSB as a polynomial function of SWH and wind speed, recognising that not only the wave
	height, but also the shape of the waves (altered by wind) has influence on the altimeter range
	bias. But this approach still exhibits some limitations, in that it imposes the type of variations
	that are allowed as a result of changes in SWH or wind speed. Currently, SSB models tend to be
	non-parametric, generally expressed in the form of a grid with SWH and wind speed as coordinates
	[e.g., Gaspar and Florens, 1998]. But several more complex multi-dimensional models are currently
	under development [e.g., Feng et al., 2010; Tran et al., 2010].
</p>
