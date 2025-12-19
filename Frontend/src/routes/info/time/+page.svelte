<h1>Time</h1>

<p>
	Time in the RADS data sets is stored as 8-byte floats in UTC seconds since a given epoch (normally
	1 January 1985 or 1 January 2000). RADS will automatically convert these values into a few common
	time scales, depending on which time variable is selected. However, irrespective of the time
	scale, the clock references to UTC, rather than an atomic clock, meaning that leap seconds may
	result in a duplication of measurement times. No provision has been made to avoid confusion
	between measurements made before and after a leap second. The time corresponds to the moment of
	reflection of the radar pulse on the sea surface and is corrected for time tag biases.
</p>
