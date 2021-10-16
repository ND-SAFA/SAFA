import { Artifact } from "@/types/domain/artifact";

const type = "requirement";

export const requirements: Artifact[] = [
  {
    name: "F5",
    body: "The UAV loads an up-to-date terrain map for its planned flight route prior to deployment.,The UAV loads an up-to-date terrain map for its planned flight route prior to deployment.",
    type,
  },
  {
    name: "F6",
    body: "The UAV shall adjust its altitude to compensate for changes in terrain based.,The UAV shall adjust its altitude to compensate for changes in terrain based.",
    type,
  },
  {
    name: "F10",
    body: "The system cedes control to the RPIC upon request,The system cedes control to the RPIC when requested using the radio controller.",
    type,
  },
  {
    name: "F11",
    body: "The system shall track GPS coordinates within 1 meter of accuracy,The system shall track GPS coordinates within 1 meter of accuracy",
    type,
  },
  {
    name: "F21",
    body: "Time to impact is computed based on velocity and direction of flight,Time to impact is computed based on velocity and direction of flight",
    type,
  },
];
