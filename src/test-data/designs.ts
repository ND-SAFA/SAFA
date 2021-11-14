import { Artifact } from "@/types";

const type = "design";

export const designs: Artifact[] = [
  {
    name: "D1",
    body: "Display warning when flying below minimum distance from ground. When a UAV is flying below a minimum threshold altitude the system shall automatically display a warning message notifying the RPIC.",
    type,
  },
  {
    name: "D2",
    body: "Alert shall be displayed when a UAV autonomously increases altitude to maintain distance from ground.",
    type,
  },
  {
    name: "D3",
    body: "All autonomous altitude adjustments taken for collision avoidance purposes are reported to the operator. All autonomous altitude adjustments taken for collision avoidance purposes are reported to the operator.",
    type,
  },
  {
    name: "D4",
    body: "Enable operator to overide autonomous decisions. The operator has the ability to override autonomous decisions to the fullest extent possible (e.g.  return to the pre-decision altitude)",
    type,
  },
  {
    name: "D5",
    body: "The UAV shall provide a description of its autonomous decisions,When requested by the user the UAV must provide a comprehensible explanation of its autonomous decisions",
    type,
  },
  {
    name: "D7",
    body: "The UAV shall modify target waypoints that are below the altitude of the terrain,The system must have an inbuilt failsafe to prevent the UAV from flying directly into the ground. In the instance that the throttle is set downwards during a hand-over event  the UAV may descend rapidly but will stop and hover before reaching the ground.",
    type,
  },

  {
    name: "D9",
    body: "When manual control is assumed all loaded missions shall be removed,Whenever manual control is assumed by the RPIC  all remaining waypoints shall be cancelled by the system immediately and the UAV should switch to hover in place. The RPIC shall receive training on how to identify the heading of a UAV by rotating the UAV clockwise and accelering periodically.",
    type,
  },
  {
    name: "D10",
    body: "Display a warning if satellite locks fall below acceptable numbers,If the number of locked sattelites falls below a threshold  the system shall automatically display a warning message  notifying the RPIC. The position inaccuracy shall be displayed in the user interface  e.g. by displaying a circle around the UAV  showing its approx. estimated position.",
    type,
  },
  {
    name: "D11",
    body: "A warning shall be generated if RTL altitudes conflict between multiple UAVs,When a UAV switches to RTL  its RTL altitude is displayed in the status bar and a warning is issued if RTL altitudes conflict (i.e.  lack minimum altitude separation) for multiple UAVs in RTL mode.",
    type,
  },
  {
    name: "F8",
    body: "Each GPS is equipped with RTK (real-time-kinematics) for accurate geolocation,Each GPS is equipped with RTK (real-time-kinematics) for accurate geolocation",
    type,
  },
  {
    name: "F9",
    body: "The system is equipped with ground-facing sensors to compute distance from the terrain.,The system is equipped with ground-facing sensors to compute distance from the terrain.",
    type,
  },
  {
    name: "F15",
    body: "The system shall provide the capability to automatically assign safe RTL altitudes.,The system shall provide the capability to automatically assign safe RTL altitudes.",
    type,
  },
  {
    name: "F16",
    body: "RTL altitudes set above legal limits shall be logged,Whenever an RTL altitude is set above legal limits a persistent log shall be created",
    type,
  },
  {
    name: "F17",
    body: "RTL altitudes shall be checked prior to flight to ensure that they are within legal limits.,RTL altitudes shall be checked prior to flight to ensure that they are within legal limits.",
    type,
  },
];
