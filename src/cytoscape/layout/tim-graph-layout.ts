import { GraphLayout, TimKlaySettings } from "./index";
import { DefaultCytoEvents } from "@/cytoscape/events";

export default class TimGraphLayout extends GraphLayout {
  constructor() {
    super({}, DefaultCytoEvents, TimKlaySettings, [], []);
  }
}
