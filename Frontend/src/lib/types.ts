type NetcdfVariable = {
    dimension: string[];
    attributes: Record<string, any>;
    values: number[];
};

export type SelectionBox = {
    northEast: L.LatLng;
    southWest: L.LatLng;
};

export type NetcdfFile = Record<string, NetcdfVariable>;
