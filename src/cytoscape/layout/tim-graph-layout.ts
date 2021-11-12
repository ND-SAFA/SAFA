import { DefaultKlayLayout } from "@/cytoscape/layout/klay-layout-settings";
import { GraphLayout } from "./index";
import { DefaultCytoEvents } from "@/cytoscape/events";

export default class TimGraphLayout extends GraphLayout {
  constructor() {
    super({}, DefaultCytoEvents, DefaultKlayLayout, [], []);
  }
}
