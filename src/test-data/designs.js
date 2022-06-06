"use strict";
exports.__esModule = true;
exports.designs = void 0;
var type = "design";
exports.designs = [
    {
        id: "2f974d28-bc1d-4461-a496-d5d3f2c14553",
        name: "D1",
        body: "Display warning when flying below minimum distance from ground. When a UAV is flying below a minimum threshold altitude the system shall automatically display a warning message notifying the RPIC.",
        type: type,
        documentIds: []
    },
    {
        id: "3bf403c7-207c-4f82-87b8-f435952aa492",
        name: "D2",
        body: "Alert shall be displayed when a UAV autonomously increases altitude to maintain distance from ground.",
        type: type,
        documentIds: []
    },
    {
        id: "687dcb2e-fd77-46e6-9c53-f6cb4c77d840",
        name: "D3",
        body: "All autonomous altitude adjustments taken for collision avoidance purposes are reported to the operator. All autonomous altitude adjustments taken for collision avoidance purposes are reported to the operator.",
        type: type,
        documentIds: []
    },
    {
        id: "f5e7dac1-90f1-4fbc-9a2a-17c87804ca31",
        name: "D4",
        body: "Enable operator to overide autonomous decisions. The operator has the ability to override autonomous decisions to the fullest extent possible (e.g.  return to the pre-decision altitude)",
        type: type,
        documentIds: []
    },
    {
        id: "8448c657-009d-4ef4-9b57-2bd4011e26bd",
        name: "D5",
        body: "The UAV shall provide a description of its autonomous decisions,When requested by the user the UAV must provide a comprehensible explanation of its autonomous decisions",
        type: type,
        documentIds: []
    },
    {
        id: "0a3379f6-4bdc-4f38-b0cf-6b0962e173a3",
        name: "D7",
        body: "The UAV shall modify target waypoints that are below the altitude of the terrain,The system must have an inbuilt failsafe to prevent the UAV from flying directly into the ground. In the instance that the throttle is set downwards during a hand-over event  the UAV may descend rapidly but will stop and hover before reaching the ground.",
        type: type,
        documentIds: []
    },
    {
        id: "a67188dc-c8a6-4c3e-acf2-900a4a7b7ad8",
        name: "D9",
        body: "When manual control is assumed all loaded missions shall be removed,Whenever manual control is assumed by the RPIC  all remaining waypoints shall be cancelled by the system immediately and the UAV should switch to hover in place. The RPIC shall receive training on how to identify the heading of a UAV by rotating the UAV clockwise and accelering periodically.",
        type: type,
        documentIds: []
    },
    {
        id: "",
        name: "D10",
        body: "Display a warning if satellite locks fall below acceptable numbers,If the number of locked sattelites falls below a threshold  the system shall automatically display a warning message  notifying the RPIC. The position inaccuracy shall be displayed in the user interface  e.g. by displaying a circle around the UAV  showing its approx. estimated position.",
        type: type,
        documentIds: []
    },
    {
        id: "",
        name: "D11",
        body: "A warning shall be generated if RTL altitudes conflict between multiple UAVs,When a UAV switches to RTL  its RTL altitude is displayed in the status bar and a warning is issued if RTL altitudes conflict (i.e.  lack minimum altitude separation) for multiple UAVs in RTL mode.",
        type: type,
        documentIds: []
    },
    {
        id: "06611020-edbd-4936-aa78-8506a923ef2d",
        name: "F8",
        body: "Each GPS is equipped with RTK (real-time-kinematics) for accurate geolocation,Each GPS is equipped with RTK (real-time-kinematics) for accurate geolocation",
        type: type,
        documentIds: []
    },
    {
        id: "bf978943-390e-44ab-8db8-00dac42522f8",
        name: "F9",
        body: "The system is equipped with ground-facing sensors to compute distance from the terrain.,The system is equipped with ground-facing sensors to compute distance from the terrain.",
        type: type,
        documentIds: []
    },
    {
        id: "8cc64646-0581-4bd7-93f4-54fcfd0547a5 \n",
        name: "F15",
        body: "The system shall provide the capability to automatically assign safe RTL altitudes.,The system shall provide the capability to automatically assign safe RTL altitudes.",
        type: type,
        documentIds: []
    },
    {
        id: "7a7ac311-d0e0-4720-8316-b83615fae171",
        name: "F16",
        body: "RTL altitudes set above legal limits shall be logged,Whenever an RTL altitude is set above legal limits a persistent log shall be created",
        type: type,
        documentIds: []
    },
    {
        id: "e9a528ea-ce45-42a8-aca9-4f0d2615b08c",
        name: "F17",
        body: "RTL altitudes shall be checked prior to flight to ensure that they are within legal limits.,RTL altitudes shall be checked prior to flight to ensure that they are within legal limits.",
        type: type,
        documentIds: []
    },
];
