export type RADSSatellite = {
    name: string,
    code: string,
}

export const satellites: RADSSatellite[] = [
    { name: 'Geosat', code: 'gs' },
    { name: 'ERS-1', code: 'e1' },
    { name: 'TOPEX', code: 'tx' },
    { name: 'Poseidon', code: 'pn' },
    { name: 'ERS-2', code: 'e2' },
    { name: 'GFO', code: 'g1' },
    { name: 'Jason-1', code: 'j1' },
    { name: 'Envisat', code: 'n1' },
    { name: 'Jason-2', code: 'j2' },
    { name: 'CryoSat-2', code: 'c2' },
    { name: 'SARAL', code: 'sa' },
    { name: 'Jason-3', code: 'j3' },
    { name: 'Sentinel-3A', code: '3a' },
    { name: 'Sentinel-3B', code: '3b' },
    { name: 'Sentinel-6A', code: '6a' },
    { name: 'SWOT nadir', code: 'sw' }
];