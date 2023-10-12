import { defineStore } from "pinia";
import { Frame } from "webstomp-client";

import {
  ActionType,
  ArtifactSchema,
  ArtifactTypeSchema,
  ChangeMessageSchema,
  ChangeSchema,
  MembershipSchema,
  NotificationApiHook,
  ProjectSchema,
  TraceLinkSchema,
  TraceMatrixSchema,
} from "@/types";
import {
  artifactStore,
  attributesStore,
  documentStore,
  getVersionApiStore,
  jobApiStore,
  jobStore,
  membersStore,
  projectStore,
  setProjectApiStore,
  stompApiStore,
  subtreeStore,
  timStore,
  traceStore,
  warningApiStore,
} from "@/hooks";
import { fillEndpoint } from "@/api";
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
        case "PROJECT":
          // (entityIds.length should be 1 and equal to projectId)
          if (change.entityIds[0] !== projectStore.projectId) return;

          return setProjectApiStore.handleClear();
        case "MEMBERS":
          // (entityIds = projectMembershipsIds)
          membersStore.deleteMembers(change.entityIds, {
            entityType: "PROJECT",
            entityId: projectStore.projectId,
          });
          break;
        case "VERSION":
          // (entityIds = project version id)
          if (change.entityIds[0] !== projectStore.versionId) return;

          return setProjectApiStore.handleClear();
        case "TYPES":
          // (entityIds = type id)
          timStore.deleteArtifactTypes(change.entityIds);
          break;
        case "TRACE_MATRICES":
          timStore.deleteTraceMatrices(change.entityIds);
          break;
        case "DOCUMENT":
          // (entityIds = document id)
          change.entityIds.forEach((id) => documentStore.removeDocument(id));
          break;
        case "ARTIFACTS":
          // (entityIds = artifact ids)
          artifactStore.deleteArtifacts(change.entityIds);
          break;
        case "TRACES":
          // (entityIds = trace link ids)
          traceStore.deleteTraceLinks(change.entityIds);
          break;
        case "WARNINGS":
          // Never called, case here for completion.
          break;
        case "JOBS":
          // (entityIds = jobId)
          change.entityIds.forEach((id) => jobStore.deleteJob(id));
          break;
        case "LAYOUT":
          // Never called, case here for completion.
          break;
        case "MODELS":
          // (entityIds = modelIds)
          projectStore.updateProject({
            models: projectStore.models.filter(
              ({ id }) => !change.entityIds.includes(id)
            ),
          });
          break;
        case "ATTRIBUTES":
          // (entityIds = attribute keys)
          attributesStore.deleteAttributes(change.entityIds);
          break;
        case "ATTRIBUTE_LAYOUTS":
          // (entityIds = attribute layout ids)
          attributesStore.deleteAttributeLayouts(change.entityIds);
          break;
      }
    }

    function createProjectSchema(change: ChangeSchema): ProjectSchema {
      const project: ProjectSchema = projectStore.project;
      switch (change.entity) {
        case "ARTIFACTS":
          project.artifacts = <ArtifactSchema[]>change.entities;
          break;
        case "TRACES":
          project.traces = <TraceLinkSchema[]>change.entities;
          break;
        case "ACTIVE_MEMBERS":
          console.log("ACTIVE MEMBERS:", change.entities);
          membersStore.setActiveMembers(<MembershipSchema[]>change.entities);
          break;
        case "WARNINGS":
          console.log("IGNORING WARNING MESSAGE");
          break;
        case "TRACE_MATRICES":
          project.traceMatrices = <TraceMatrixSchema[]>change.entities;
          break;
        case "TYPES":
          project.artifactTypes = <ArtifactTypeSchema[]>change.entities;
          break;
        default:
          throw Error("Unhandled entity: " + change.entity);
      }
      return project;
    }

    /**
     * Updates stored project information.
     *
     * @param change - The update change.
     */
    async function handleUpdateChange(
      change: ChangeSchema,
      project: ProjectSchema
    ) {
      console.log("UPDATING: ", change);
      const versionId = projectStore.versionId;

      switch (change.entity) {
        case "PROJECT":
          projectStore.updateProject({
            name: project.name,
            description: project.description,
          });
          break;
        case "MEMBERS":
          membersStore.updateMembers(project.members, {
            entityType: "PROJECT",
            entityId: project.projectId,
          });
          break;
        case "VERSION":
          return getVersionApiStore.handleLoad(versionId);
        case "TYPES":
          timStore.addOrUpdateArtifactTypes(project.artifactTypes);
          break;
        case "TRACE_MATRICES":
          timStore.addOrUpdateTraceMatrices(project.traceMatrices);
          break;
        case "DOCUMENT":
          await documentStore.updateDocuments(project.documents);
          break;
        case "ARTIFACTS":
          console.log("ADDING OR UPDATING:", project.artifacts);
          artifactStore.addOrUpdateArtifacts(project.artifacts);
          break;
        case "TRACES":
          traceStore.addOrUpdateTraceLinks(project.traces);
          break;
        case "WARNINGS":
          return warningApiStore.handleReload(versionId);
        case "JOBS":
          return jobApiStore.handleReload();
        case "LAYOUT":
          documentStore.updateBaseLayout(project.layout);
          break;
        case "SUBTREES":
          subtreeStore.initializeProject(project);
          break;
        case "MODELS":
          projectStore.updateProject({ models: project.models });
          break;
        case "ATTRIBUTES":
          attributesStore.updateAttributes(project.attributes || []);
          break;
        case "ATTRIBUTE_LAYOUTS":
          attributesStore.updateAttributeLayouts(
            project.attributeLayouts || []
          );
          break;
      }
    }

    /**
     * Handles changes messages by updating affected parts of the app.
     *
     * @param frame - The message describing changes.
     */
    async function handleEntityChangeMessage(frame: Frame): Promise<void> {
      const message: ChangeMessageSchema = JSON.parse(frame.body);
      const project = await getChanges(versionId, message);
      let hasLayoutChange = false; // Layout changes are currently disabled.
      console.log("HANDLING MESSAGE:", message);

      // Step - Iterate through message and delete entities.
      for (const change of message.changes) {
        console.log("CURR CHANGE:", change);
        const project = createProjectSchema(change);
        if (change.action === ActionType.DELETE) {
          console.log("Handling DELETE>");
          await handleDeleteChange(change);
        } else if (change.action === ActionType.UPDATE) {
          console.log("STARTING CHANGE", project);
          await handleUpdateChange(change, project);
        } else {
          throw Error("Unable to handle action:" + change.action);
        }
        console.log("Done with change.");
      }
    }

    async function handleSubscribeVersion(
      projectId: string,
      versionId: string
    ): Promise<void> {
      if (!projectId || !versionId) return;

      await stompApiStore.connectStomp();

      stompApiStore.clearStompSubscriptions();

      await stompApiStore.subscribeToStomp(
        fillEndpoint("projectTopic", { projectId }),
        handleEntityChangeMessage
      );

      await stompApiStore.subscribeToStomp(
        fillEndpoint("versionTopic", { versionId }),
        handleEntityChangeMessage
      );
    }

    return { handleSubscribeVersion };
  }
);

export default useNotificationApi(pinia);
