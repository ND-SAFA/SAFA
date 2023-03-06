import { KlayLayoutSettings } from "@/types";
import {
  LAYOUT_ALIGNMENT,
  LAYOUT_NODE_DIRECTION,
  LAYOUT_NODE_LAYERING,
  LAYOUT_NODE_PLACEMENT,
  LAYOUT_NODE_SPACING,
  LAYOUT_RANDOM_SEED,
  LAYOUT_THOROUGHNESS,
  LAYOUT_USE_HIERARCHY,
} from "@/cytoscape/styles";

// docs: https://github.com/cytoscape/cytoscape.js-klay
export const TimKlaySettings: KlayLayoutSettings = {
  spacing: LAYOUT_NODE_SPACING,
  direction: LAYOUT_NODE_DIRECTION,
  fixedAlignment: LAYOUT_ALIGNMENT,
  layoutHierarchy: LAYOUT_USE_HIERARCHY,
  nodeLayering: LAYOUT_NODE_LAYERING,
  nodePlacement: LAYOUT_NODE_PLACEMENT,
  thoroughness: LAYOUT_THOROUGHNESS,
  randomizationSeed: LAYOUT_RANDOM_SEED,
};
