<h1>Altimeter range RMS</h1>

<p>
	The altimeter ranges are provided in RADS as (approximately) 1-second averages based on 10, 20, or
	40 ’elementary’ measurements during that second. The altimeter range reported is, in fact, not the
	statistical mean, but is generally determined as follows: Interpolate the orbital altitude at the
	same time tags as the elementary measurements; Subtract the orbital altitude from the range; Fit a
	linear trend true ‘range minus orbit’; Remove the linear trend; Compute the standard deviation of
	the residuals (using n − 2 in the denominator) where n is the number of elementary measurements
	during a 1-Hz period; Evaluate the linear trend at the mid point and add the local orbital
	altitude back at this point to obtain the average range. Hence, technically, range rms is not the
	standard deviation of the altimeter range, but the stan- dard deviation of the elementary ‘orbit
	minus range’ values with a trend fitted and removed as well, and taking into account the extra
	degree of freedom. It should also not be confused with an error estimate for the range
	measurement.
</p>
