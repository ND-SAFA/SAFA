import { Frame } from "webstomp-client";
import {
  Action,
  Change,
  Entity,
  EntityChangeMessage,
  ProjectModel,
} from "@/types";
import { getChanges } from "@/api/endpoints/sync-api";

export async function handleEntityChangeMessage(
  versionId: string,
  frame: Frame
) {
  const message: EntityChangeMessage = JSON.parse(frame.body);
  const project: ProjectModel = await getChanges(versionId, message);

  // Step - Iterate through message and delete entities
  for (
    let changeIndex = 0;
    changeIndex < message.changes.length;
    changeIndex++
  ) {
    const change: Change = message.changes[changeIndex];
    if (change.action === Action.DELETE) {
      handleDeleteChange(change.entity, change.entityIds);
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
 * For a change marking the deletion of some entities,
 * this removes those entities from the store.
 * @param change
 */
function handleDeleteChange(entity: Entity, entityIds: string[]) {
  switch (entity) {
    case Entity.PROJECT:
      //(entityIds.length should be 1 and equal to projectId)
      break;
    case Entity.MEMBERS:
      // (entityIds = projectMembershipsIds)
      break;
    case Entity.VERSION:
      // (entityIds = project version id)
      break;
    case Entity.TYPES:
      // (entityIds = type id)
      break;
    case Entity.DOCUMENT:
      // (entityIds = document id)
      break;
    case Entity.ARTIFACTS:
      // (entityIds = artifact ids)
      break;
    case Entity.TRACES:
      // (entityIds = trace link ids)
      break;
    case Entity.WARNINGS:
      // Never called, case here for completion.
      break;
    case Entity.JOBS:
      // (entityIds = jobId)
      break;
    default:
      throw Error("Unknown entity type:" + entity);
  }
}
