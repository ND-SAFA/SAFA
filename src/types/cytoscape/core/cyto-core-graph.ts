import cytoscape, { CytoscapeOptions } from "cytoscape";
import { CytoCore } from "@/types/cytoscape/core";

/**
 * Background: Cytoscape has to be wrapped in a promise in order to
 * wait for all elements to be loaded into the instance.
 *
 * See issue: https://github.com/rcarcasses/vue-cytoscape/issues/50
 */

/**
 * Wraps cytoscape instance in a promise.
 */
export type ResolveCy =
  | ((value: CytoCore | PromiseLike<CytoCore>) => void)
  | null;

/**
 * Returns an instance of cytoscape when all elements have
 * been loaded
 */
export type CyPromise = Promise<CytoCore>;

/**
 * Defines a plugin to be used on cytoscape
 */
export interface CytoCorePlugin {
  initialize: (cy: typeof cytoscape) => void;
  afterInit: (cy: CytoCore) => void;
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
  afterInit: (cy: CytoCore) => void;
}
