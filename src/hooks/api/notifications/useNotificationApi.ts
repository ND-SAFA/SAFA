import { defineStore } from "pinia";
import { Frame } from "webstomp-client";

import {
  ActionType,
  ChangeMessageSchema,
  ChangeSchema,
  EntityType,
  NotificationApiHook,
  notifyUserEntities,
  ProjectSchema,
} from "@/types";
import {
  appStore,
  artifactStore,
  attributesStore,
  documentStore,
  jobStore,
  membersStore,
  projectStore,
  subtreeStore,
  traceStore,
  logStore,
  stompApiStore,
  setProjectApiStore,
  getVersionApiStore,
  jobApiStore,
  warningApiStore,
  timStore,
} from "@/hooks";
import { router } from "@/router";
import { Endpoint, fillEndpoint, getChanges } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing notification API requests.
 */
export const useNotificationApi = defineStore(
  "notificationApi",
  (): NotificationApiHook => {
    /**
     * Deletes stored project information.
     *
     * @param change - The deletion change.
     */
    async function handleDeleteChange(change: ChangeSchema) {
      switch (change.entity) {
        case EntityType.PROJECT:
          // (entityIds.length should be 1 and equal to projectId)
          if (change.entityIds[0] !== projectStore.projectId) return;

          return setProjectApiStore.handleClear();
        case EntityType.MEMBERS:
          // (entityIds = projectMembershipsIds)
          membersStore.deleteMembers(change.entityIds);
          break;
        case EntityType.VERSION:
          // (entityIds = project version id)
          if (change.entityIds[0] !== projectStore.versionId) return;

          return setProjectApiStore.handleClear();
        case EntityType.TYPES:
          // (entityIds = type id)
          timStore.deleteArtifactTypes(change.entityIds);
          break;
        case EntityType.TRACE_MATRICES:
          timStore.deleteTraceMatrices(change.entityIds);
          break;
        case EntityType.DOCUMENT:
          // (entityIds = document id)
          change.entityIds.forEach((id) => documentStore.removeDocument(id));
          break;
        case EntityType.ARTIFACTS:
          // (entityIds = artifact ids)
          artifactStore.deleteArtifacts(change.entityIds);
          break;
        case EntityType.TRACES:
          // (entityIds = trace link ids)
          traceStore.deleteTraceLinks(change.entityIds);
          break;
        case EntityType.WARNINGS:
          // Never called, case here for completion.
          break;
        case EntityType.JOBS:
          // (entityIds = jobId)
          change.entityIds.forEach((id) => jobStore.deleteJob(id));
          break;
        case EntityType.LAYOUT:
          // Never called, case here for completion.
          break;
        case EntityType.MODELS:
          // (entityIds = modelIds)
          projectStore.updateProject({
            models: projectStore.models.filter(
              ({ id }) => !change.entityIds.includes(id)
            ),
          });
          break;
        case EntityType.ATTRIBUTES:
          // (entityIds = attribute keys)
          attributesStore.deleteAttributes(change.entityIds);
          break;
        case EntityType.ATTRIBUTE_LAYOUTS:
          // (entityIds = attribute layout ids)
          attributesStore.deleteAttributeLayouts(change.entityIds);
          break;
      }
    }

    /**
     * Updates stored project information.
     *
     * @param change - The update change.
     * @param project - The updated project.
     */
    async function handleUpdateChange(
      change: ChangeSchema,
      project: ProjectSchema
    ) {
      const versionId = projectStore.versionId;

      switch (change.entity) {
        case EntityType.PROJECT:
          projectStore.updateProject({
            name: project.name,
            description: project.description,
          });
          break;
        case EntityType.MEMBERS:
          membersStore.updateMembers(project.members, {
            entityType: "PROJECT",
            entityId: project.projectId,
          });
          break;
        case EntityType.VERSION:
          return getVersionApiStore.handleLoad(versionId);
        case EntityType.TYPES:
          timStore.addOrUpdateArtifactTypes(project.artifactTypes);
          break;
        case EntityType.TRACE_MATRICES:
          timStore.addOrUpdateTraceMatrices(project.traceMatrices);
          break;
        case EntityType.DOCUMENT:
          await documentStore.updateDocuments(project.documents);
          break;
        case EntityType.ARTIFACTS:
          artifactStore.addOrUpdateArtifacts(project.artifacts);
          break;
        case EntityType.TRACES:
          traceStore.addOrUpdateTraceLinks(project.traces);
          break;
        case EntityType.WARNINGS:
          return warningApiStore.handleReload(versionId);
        case EntityType.JOBS:
          return jobApiStore.handleReload();
        case EntityType.LAYOUT:
          documentStore.updateBaseLayout(project.layout);
          break;
        case EntityType.SUBTREES:
          subtreeStore.initializeProject(project);
          break;
        case EntityType.MODELS:
          projectStore.updateProject({ models: project.models });
          break;
        case EntityType.ATTRIBUTES:
          attributesStore.updateAttributes(project.attributes || []);
          break;
        case EntityType.ATTRIBUTE_LAYOUTS:
          attributesStore.updateAttributeLayouts(
            project.attributeLayouts || []
          );
          break;
      }
    }

    /**
     * Handles changes messages by updating affected parts of the app.
     *
     * @param versionId - The project version being updated.
     * @param frame - The message describing changes.
     */
    async function handleEntityChangeMessage(
      versionId: string,
      frame: Frame
    ): Promise<void> {
      const routeRequiresProject = router.currentRoute.value.matched.some(
        ({ meta }) => meta.requiresProject
      );
      const message: ChangeMessageSchema = JSON.parse(frame.body);
      const project = await getChanges(versionId, message);
      let hasLayoutChange = false;

      // Step - Iterate through message and delete entities.
      for (const change of message.changes) {
        if (!notifyUserEntities.includes(change.entity)) return;

        if (change.action === ActionType.DELETE) {
          await handleDeleteChange(change);
        } else if (change.action === ActionType.UPDATE) {
          await handleUpdateChange(change, project);

          if (change.entity === EntityType.ARTIFACTS) {
            hasLayoutChange = true;
          }
        }
      }

      // Step - Update default layout if needed.
      if (!routeRequiresProject || !hasLayoutChange) return;

      appStore.enqueueChanges(async () => {
        documentStore.updateBaseLayout(project.layout);
      });
    }

    async function handleSubscribeVersion(
      projectId: string,
      versionId: string
    ): Promise<void> {
      if (!projectId || !versionId) return;

      await stompApiStore.connectStomp();

      stompApiStore.clearStompSubscriptions();

      await stompApiStore.subscribeToStomp(
        fillEndpoint(Endpoint.projectTopic, { projectId }),
        (frame) =>
          handleEntityChangeMessage(versionId, frame).catch((e) =>
            logStore.onError(e)
          )
      );

      await stompApiStore.subscribeToStomp(
        fillEndpoint(Endpoint.versionTopic, { versionId }),
        (frame) =>
          handleEntityChangeMessage(versionId, frame).catch((e) =>
            logStore.onError(e)
          )
      );
    }

    return { handleSubscribeVersion };
  }
);

export default useNotificationApi(pinia);
