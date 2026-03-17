export type RADSSatellite = {
    name: string,
    code: string,
    start: string,
    end: string,
}

export const satellites: RADSSatellite[] = [
    { 
        name: 'Geosat', 
        code: 'gs', 
        start: "1985-03-13", 
        end: "1989-12-31" 
    },
    { 
        name: 'ERS-1', 
        code: 'e1', 
        start: "1991-08-30",
        end: "1996-06-03"
    },    
    { 
        name: 'ERS-2', 
        code: 'e2',
        start: "1995-04-30",
        end: "2011-07-05" 
    },
    { 
        name: 'TOPEX', 
        code: 'tx',
        start: "1995-10-14",
        end: "2005-10-05"
    },
    { 
        name: 'Poseidon', 
        code: 'pn',
        start: "1992-10-22",
        end: "2002-07-13"
    },
    { 
        name: 'GFO', 
        code: 'g1',
        start: "2000-01-08",
        end: "2008-09-17"
    },    
    { 
        name: 'Envisat', 
        code: 'n1', 
        start: "2002-05-15",
        end: "2012-04-08"
    },
    { 
        name: 'Jason-1', 
        code: 'j1', 
        start:"2002-01-16",
        end: "2013-06-22"
    },
    { 
        name: 'Jason-2', 
        code: 'j2', 
        start:"2008-07-05",
        end: "2019-10-02"
    },
    { 
        name: 'Jason-3', 
        code: 'j3', 
        start: "2016-02-13",
        end: "present"
    },
    { 
        name: 'CryoSat-2', 
        code: 'c2', 
        start: "2010-07-17",
        end: "present"
    },
    { 
        name: 'SARAL', 
        code: 'sa',
        start: "2013-03-15",
        end: "present",
    },
    { 
        name: 'Sentinel-3A', 
        code: '3a', 
        start: "2016-03-02",
        end: "present"
    },
    { 
        name: 'Sentinel-3B', 
        code: '3b', 
        start: "2018-06-07",
        end: "present"
    },
    { 
        name: 'Sentinel-6A', 
        code: '6a', 
        start: "2020-12-18",
        end: "present"
    },
    { 
        name: 'SWOT nadir', 
        code: 'sw', 
        start: "2023-01-17",
        end: "present"
    }
];