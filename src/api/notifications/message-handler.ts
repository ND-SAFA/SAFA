import { Frame } from "webstomp-client";
import {
  ActionType,
  ChangeModel,
  EntityType,
  ChangeMessageModel,
} from "@/types";
import { getChanges } from "@/api/endpoints/sync-api";

/**
 * Handles changes messages by updating affected parts of the app.
 *
 * @param versionId - The project version being updated.
 * @param frame - The message describing changes.
 */
export async function handleEntityChangeMessage(
  versionId: string,
  frame: Frame
): Promise<void> {
  const message: ChangeMessageModel = JSON.parse(frame.body);
  const project = await getChanges(versionId, message);

  // Step - Iterate through message and delete entities
  for (const change of message.changes) {
    if (change.action === ActionType.DELETE) {
      handleDeleteChange(change);
    }
  }

  // Step - Update default layout
  if (message.updateLayout) {
    // TODO: Set project layout (updated layout included in project.layout)
  }

  // Step - TODO: Update documents + layouts
  // Step - TODO: Add or update artifacts if non-empty(project.artifacts)
  // Step - TODO: Add or update traces if non-empty (project.traces);
  // Step - TODO: Update warnings if non-empty (projet.warnings))
}

/**
 * Deletes stored objects in the store.
 *
 * @param change - The deletion change.
 */
function handleDeleteChange(change: ChangeModel) {
  switch (change.entity) {
    case EntityType.PROJECT:
      //(entityIds.length should be 1 and equal to projectId)
      break;
    case EntityType.MEMBERS:
      // (entityIds = projectMembershipsIds)
      break;
    case EntityType.VERSION:
      // (entityIds = project version id)
      break;
    case EntityType.TYPES:
      // (entityIds = type id)
      break;
    case EntityType.DOCUMENT:
      // (entityIds = document id)
      break;
    case EntityType.ARTIFACTS:
      // (entityIds = artifact ids)
      break;
    case EntityType.TRACES:
      // (entityIds = trace link ids)
      break;
    case EntityType.WARNINGS:
      // Never called, case here for completion.
      break;
    case EntityType.JOBS:
      // (entityIds = jobId)
      break;
  }
}
