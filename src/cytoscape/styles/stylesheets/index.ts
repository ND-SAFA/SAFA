import { CytoscapeStyle } from "@/cytoscape/styles/stylesheets/cytoscape";
import { EdgeHandlesStyle } from "@/cytoscape/styles/stylesheets/edge-handles";

export const GraphStyle = CytoscapeStyle.concat(EdgeHandlesStyle);

export * from "./cytoscape";
export * from "./edge-handles";
