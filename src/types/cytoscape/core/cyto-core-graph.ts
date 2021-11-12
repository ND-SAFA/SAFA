import { CytoCore } from "@/types/cytoscape/core";
import { CytoscapeOptions } from "cytoscape";

// waits for elements to be added to cytoscape instance before returning
// see: https://github.com/rcarcasses/vue-cytoscape/issues/50
export type ResolveCy =
  | ((value: CytoCore | PromiseLike<CytoCore>) => void)
  | null;

/**
 * A generic function type using a CytoCore instance.
 */
export type CytoCoreAction = (cy: CytoCore) => void;

/**
 * Defines an plugin to be used on cytoscape
 */
export interface CytoCorePlugin {
  plugin: CytoCoreAction;
  afterInit: CytoCoreAction;
}

/**
 * Defines the necessary components to setup a cytoscape graph including:
 */
export interface CytoCoreGraph {
  /**
   * Name to be used for error messages.
   */
  name: string;
  /**
   * Defines initial configuration settings the graph should have.
   */
  config: CytoscapeOptions;
  /**
   * Resolution function to store unique cytoscape instance
   */
  saveCy: ResolveCy;
  /**
   * List of plugins that are installed onto cytoscape instance.
   */
  plugins: CytoCorePlugin[];
  /**
   * Handler for performing any actions once all plugins and elements have
   * been setup in cytoscape instance.
   */
  afterInit: CytoCoreAction;
}
