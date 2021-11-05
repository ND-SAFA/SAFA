import { Artifact } from "@/types";

const type = "hazard";

export const hazards: Artifact[] = [
  {
    name: "F3",
    body: "The UAV crashes into the terrain or another object right after an operator manually assumes control of the system from the computerized system.,The UAV crashes into the terrain or another object right after an operator manually assumes control of the system from the computerized system.",
    type,
  },
  {
    name: "F4",
    body: "Minimum separation distance is violated between airborne UAVs,Minimum separation distance and or time-to-impact threshold is violated between airborne UAVs",
    type,
  },
  {
    name: "F1",
    body: "A UAV flies dangerously close to another object,A UAV flies dangerously close to another object",
    type,
  },
  {
    name: "F2",
    body: "A UAV flies too close to ground-based objects (e.g.  ground  trees  buildings  people),A UAV flies too close to ground-based objects (e.g.  ground  trees  buildings  people)",
    type,
  },
  {
    name: "F20",
    body: "The collision avoidance system malfunctions,The collision avoidance system malfunctions",
    type,
  },
];
