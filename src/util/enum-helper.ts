import { DocumentType, SafetyCaseType } from "@/types";

/**
 * Returns display names for each document type.
 */
export function documentTypeOptions(): { id: string; name: string }[] {
  return [
    { id: DocumentType.ARTIFACT_TREE, name: "Default" },
    { id: DocumentType.FTA, name: "FTA" },
    { id: DocumentType.SAFETY_CASE, name: "Safety Case" },
  ];
}

/**
 * Returns display names for each safety case type.
 */
export function safetyCaseOptions(): { id: string; name: string }[] {
  return [
    { id: SafetyCaseType.CONTEXT, name: "Context" },
    { id: SafetyCaseType.GOAL, name: "Goal" },
    { id: SafetyCaseType.STRATEGY, name: "Strategy" },
    { id: SafetyCaseType.SOLUTION, name: "Solution" },
  ];
}
