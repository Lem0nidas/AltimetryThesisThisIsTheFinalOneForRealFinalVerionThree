type NetcdfVariable = {
    dimension: string[];
    attributes: Record<string, any>;
    values: number[];
};

export type NetcdfFile = Record<string, NetcdfVariable>;
