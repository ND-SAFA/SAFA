import { CytoscapeStyle } from "./base";
import { EdgeHandlesStyle } from "./edge-handles";

export const GraphStyle = [...CytoscapeStyle, ...EdgeHandlesStyle];

export * from "./base";
export * from "./edge-handles";
export * from "./tim-styles";
