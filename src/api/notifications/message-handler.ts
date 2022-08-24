import { Frame } from "webstomp-client";
import {
  ActionType,
  ChangeModel,
  EntityType,
  ChangeMessageModel,
  ProjectModel,
} from "@/types";
import { getChanges } from "@/api/endpoints/sync-api";
import {
  handleClearProject,
  handleLoadVersion,
  handleReloadJobs,
  handleReloadWarnings,
} from "@/api";
import { documentStore, jobStore, projectStore } from "@/hooks";

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

  // Step - Iterate through message and delete entities.
  for (const change of message.changes) {
    if (change.action === ActionType.DELETE) {
      await handleDeleteChange(change);
    } else {
      await handleUpdateChange(change, project);
    }
  }

  // Step - Update default layout.
  if (message.updateLayout) {
    projectStore.updateLayout(project.layout);
  }
}

/**
 * Deletes stored project information.
 *
 * @param change - The deletion change.
 */
async function handleDeleteChange(change: ChangeModel) {
  switch (change.entity) {
    case EntityType.PROJECT:
      // (entityIds.length should be 1 and equal to projectId)
      if (change.entityIds[0] !== projectStore.projectId) return;

      return handleClearProject();
    case EntityType.MEMBERS:
      // (entityIds = projectMembershipsIds)
      projectStore.deleteMembers(change.entityIds);
      break;
    case EntityType.VERSION:
      // (entityIds = project version id)
      if (change.entityIds[0] !== projectStore.versionId) return;

      return handleClearProject();
    case EntityType.TYPES:
      // (entityIds = type id)
      projectStore.removeArtifactTypes(change.entityIds);
      break;
    case EntityType.DOCUMENT:
      // (entityIds = document id)
      documentStore.removeDocument(change.entityIds[0]);
      break;
    case EntityType.ARTIFACTS:
      // (entityIds = artifact ids)
      projectStore.deleteArtifacts(change.entityIds);
      break;
    case EntityType.TRACES:
      // (entityIds = trace link ids)
      projectStore.deleteTraceLinks(change.entityIds);
      break;
    case EntityType.WARNINGS:
      // Never called, case here for completion.
      break;
    case EntityType.JOBS:
      // (entityIds = jobId)
      jobStore.deleteJob(change.entityIds[0]);
      break;
    case EntityType.LAYOUT:
      // Never called, case here for completion.
      break;
  }
}

/**
 * Updates stored project information.
 *
 * @param change - The update change.
 * @param project - The updated project.
 */
async function handleUpdateChange(change: ChangeModel, project: ProjectModel) {
  const versionId = project.projectVersion?.versionId || "";

  switch (change.entity) {
    case EntityType.PROJECT:
      projectStore.updateProject({
        name: project.name,
        description: project.description,
      });
      break;
    case EntityType.MEMBERS:
      projectStore.updateMembers(project.members);
      break;
    case EntityType.VERSION:
      if (versionId !== projectStore.versionId) return;

      return handleLoadVersion(versionId);
    case EntityType.TYPES:
      projectStore.addOrUpdateArtifactTypes(project.artifactTypes);
      break;
    case EntityType.DOCUMENT:
      documentStore.updateDocuments(project.documents);
      break;
    case EntityType.ARTIFACTS:
      projectStore.addOrUpdateArtifacts(project.artifacts);
      break;
    case EntityType.TRACES:
      projectStore.addOrUpdateTraceLinks(project.traces);
      break;
    case EntityType.WARNINGS:
      return handleReloadWarnings(versionId);
    case EntityType.JOBS:
      return handleReloadJobs();
    case EntityType.LAYOUT:
      projectStore.updateLayout(project.layout);
      break;
  }
}
