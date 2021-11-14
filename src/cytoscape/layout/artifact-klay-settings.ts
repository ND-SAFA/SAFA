import { KlayLayoutSettings } from "@/types";
import {
  LAYOUT_NODE_SPACING,
  LAYOUT_NODE_DIRECTION,
  LAYOUT_ALIGNMENT,
  LAYOUT_USE_HIERARCHY,
  LAYOUT_NODE_LAYERING,
  LAYOUT_NODE_PLACEMENT,
  LAYOUT_THOROUGHNESS,
  LAYOUT_NODE_INNER_SPACING,
  LAYOUT_RANDOM_SEED,
} from "@/cytoscape/styles";

// docs: https://github.com/cytoscape/cytoscape.js-klay
export const ArtifactKlaySettings: KlayLayoutSettings = {
  spacing: LAYOUT_NODE_SPACING,
  direction: LAYOUT_NODE_DIRECTION,
  fixedAlignment: LAYOUT_ALIGNMENT,
  layoutHierarchy: LAYOUT_USE_HIERARCHY,
  nodeLayering: LAYOUT_NODE_LAYERING,
  nodePlacement: LAYOUT_NODE_PLACEMENT,
  inLayerSpacingFactor: LAYOUT_NODE_INNER_SPACING,
  thoroughness: LAYOUT_THOROUGHNESS,
  randomizationSeed: LAYOUT_RANDOM_SEED,
};
