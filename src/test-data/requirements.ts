import { Artifact } from "@/types";

const type = "requirement";

export const requirements: Artifact[] = [
  {
    id: "5aa82e59-1f02-4465-9555-95b7a75668c0",
    name: "F5",
    body: "The UAV loads an up-to-date terrain map for its planned flight route prior to deployment.,The UAV loads an up-to-date terrain map for its planned flight route prior to deployment.",
    type,
    documentIds: [],
  },
  {
    id: "b15df816-825c-439c-b1a4-bf4e25f7c076",
    name: "F6",
    body: "The UAV shall adjust its altitude to compensate for changes in terrain based.,The UAV shall adjust its altitude to compensate for changes in terrain based.",
    type,
    documentIds: [],
  },
  {
    id: "30ddc8b2-9ffd-4384-b0f2-5249b81abf8b",
    name: "F10",
    body: "The system cedes control to the RPIC upon request,The system cedes control to the RPIC when requested using the radio controller.",
    type,
    documentIds: [],
  },
  {
    id: "cfb33728-ac77-4ef0-9bcf-34d31262e01b",
    name: "F11",
    body: "The system shall track GPS coordinates within 1 meter of accuracy,The system shall track GPS coordinates within 1 meter of accuracy",
    type,
    documentIds: [],
  },
  {
    id: "e2dcbdea-a30a-427f-9193-6b30b1356d6d",
    name: "F21",
    body: "Time to impact is computed based on velocity and direction of flight,Time to impact is computed based on velocity and direction of flight",
    type,
    documentIds: [],
  },
];
