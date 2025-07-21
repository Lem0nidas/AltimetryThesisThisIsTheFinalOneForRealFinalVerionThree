export type RADSVariable = {
    name: string,
    varName: string,
    description: string,
}

export const variables: RADSVariable[] = [
    {
        name: 'Time', 
        varName: 'time', 
        description: 'Time in seconds since 1985-01-01 00:00:00.'
    },
    {
        name: 'Latitude', 
        varName: 'lat', 
        description: 'Degrees relative to equator. Postive towards north.'
    },
    {
        name: 'Longitude', 
        varName: 'lon', 
        description: 'Degrees realative to Greenwich meridian. Positive towards east.'
    },
    {
        name: 'Orbital altitude', 
        varName: 'alt', 
        description: 
        `The orbital altitude is the height of the centre-of-mass of the satellite 
        above the TOPEX reference ellipsoid (semi-major axis = 6378136.3 m, 
        inverse flattening = 298.257) as computed by satellite orbit determination.`
    },
    { 
        name: 'Sea Level Anomaly', 
        varName: 'sla', 
        description: 
        `The sea level anomaly (SLA) is the height for the sea surface 
        relative to a long term mean.`
    },
    {
        name: 'Sea Surface Height Anomaly (Precomputed SLA)', 
        varName: 'ssha', 
        description: 
        `The sea level anomaly (SLA) is the height for the sea surface 
        relative to a long term mean. The SSHA is precomputed and uneditable SLA`
    },
    {
        name: 'Altimeter Range', 
        varName: 'range', 
        description: 'The range between the satellite and the sea surface'
    },
    {
        name: 'Altimeter Range RMS', 
        varName: 'range_rms', 
        description: 'Standard deviation of the `Orbit minus range` values'
    },
    {
        name: 'Dry Tropospheric Correction', 
        varName: 'dry_tropo', 
        description: 'Delay of the radar signal in the atmoshpere, not counting the effect of water vapour.'
    },
    {
        name: 'Wet Tropospheric Correction', 
        varName: 'wet_tropo', 
        description: 'Delay of the signal in the atmosphere due to the presence of water vapours.'
    },
    {
        name: 'Ionospheric Correction', 
        varName: 'iono', 
        description: 
        `The radar signal is also delayed by ions and electrons 
        in the upper layers of the atmosphere (the ionosphere)`
    },
    {
        name: 'Atmospheric (Inverse Barometer) Correction', 
        varName: 'dac', 
        description: 
        `The inverse barometer (IB) correction accounts for the suppression of sea level 
        due to higher sea level pressure, and its rise during lower sea level pressure.`
    },
    {
        name: 'Solid Earth Tide', 
        varName: 'tide_solid', 
        description: 
        `The solid earth tide is the variation of the elevation of the crust of the earth surface 
        as a result of the attraction by the sun and moon (other planets are generally ignored 
        as their influence is at least an order of magnitude smaller).`
    },
    {
        name: 'Pole Tide',
        varName: 'tide_pole',
        description: 
        `The pole tide is the vertical deformation of the earth crust as a result of polar motion.`
    },
    {
        name: 'Ocean Tide',
        varName: 'tide_ocean',
        description: 
        `The (pure) ocean tide is the variation of the height of the water column 
        as a result of luni-solar attraction.`
    },
    {
        name: 'Load Tide', 
        varName: 'tide_load', 
        description: 'The load tide is the effect of the tides weighing on the elastic earth.'
    },
    {
        name: 'Internal Tide',
        varName: 'tide_internal',
        description: 
        `In places where ocean topography changes significantly, the predominant barotropic tides are
        converted to baroclinic tides, which then also produce an expression in the sea surface with 
        much smaller wavelengths than the normal solar-lunar ocean tides.`
    },
    {
        name: 'Sea State Bias',
        varName: 'ssb',
        description: 
        `Sea state bias (SSB) is the term used for any altimetric range offset as a function of the 
        sea state (wave height, wind speed, wave age, swell).`
    },
    {
        name: 'Mean Sea Surface',
        varName: 'mss',
        description: 
        `The sea level anomaly (SLA) is expressed as the difference of the instantaneous 
        tide-corrected sea surface with respect to a well-established mean. 
        Over the years several (more or less) global mean sea surface models have been developed 
        from the compilation of satellite altimeter (and sometimes gravity) data.`
    },
    {
        name: 'Geoid',
        varName: 'geoid',
        description: 
        `The theoretical mean sea surface in absence of ocean currents, wind, etc. 
        Geoid models are generally made from satellite tracking data.`
    },
    {
        name: 'Significant Wave Height',
        varName: 'swh',
        description: 
        `The significant wave height (SWH) is generally defined as the mean wave height 
        (peak to trough) of the highest one-third of the ocean waves.`
    },
    {
        name: 'Wind Speed',
        varName: 'wind_speed',
        description: 'Altimeter wind speed'
    },
    {
        name: 'Bathymetry & Topography',
        varName: 'topo',
        description: 
        `Bathymetry is the depth of the oceans (and seas). It is given as a negative number, 
        and thus constitutes the elevation of the sea bottom with respect to the geoid.`
    },
];