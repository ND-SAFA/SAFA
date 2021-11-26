import { Artifact } from "@/types";

const type = "hazard";

export const hazards: Artifact[] = [
  {
    id: "0eddedcd-1020-4fb7-936e-847ab4702a80",
    name: "F3",
    body: "The UAV crashes into the terrain or another object right after an operator manually assumes control of the system from the computerized system.,The UAV crashes into the terrain or another object right after an operator manually assumes control of the system from the computerized system.",
    type,
  },
  {
    id: "ce76e8b7-25ef-4e6d-a118-757c3473c2d7",
    name: "F4",
    body: "Minimum separation distance is violated between airborne UAVs,Minimum separation distance and or time-to-impact threshold is violated between airborne UAVs",
    type,
  },
  {
    id: "3e1d08f3-69d4-4559-9159-359f88791e29",
    name: "F1",
    body: "A UAV flies dangerously close to another object,A UAV flies dangerously close to another object",
    type,
  },
  {
    id: "7dd6b6f7-aed1-4145-b50e-ad63b9597046",
    name: "F2",
    body: "A UAV flies too close to ground-based objects (e.g.  ground  trees  buildings  people),A UAV flies too close to ground-based objects (e.g.  ground  trees  buildings  people)",
    type,
  },
  {
    id: "c46e0f51-7e4b-4fd6-9690-a54c56b1aefe",
    name: "F20",
    body: "The collision avoidance system malfunctions,The collision avoidance system malfunctions",
    type,
  },
];
