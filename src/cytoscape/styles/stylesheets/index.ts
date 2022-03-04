import { CytoscapeStyle } from "./base-styles";
import { EdgeHandlesStyle } from "./edge-styles";

export const GraphStyle = [...CytoscapeStyle, ...EdgeHandlesStyle];

export * from "./base-styles";
export * from "./edge-styles";
export * from "./tim-styles";
