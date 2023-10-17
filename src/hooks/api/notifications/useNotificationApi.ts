import { defineStore, MutationType } from "pinia";
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
  StompChannel,
  TraceLinkSchema,
  TraceMatrixSchema,
} from "@/types";
import { buildProject, isProjectTopic } from "@/util";
import {
  artifactStore,
  attributesStore,
  documentStore,
  getVersionApiStore,
  jobApiStore,
  jobStore,
  logStore,
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
     * Converts a change into updated project data.
     *
     * @param change - The change.
     */
    function createProjectSchema(change: ChangeSchema): ProjectSchema {
      const project = buildProject();

      switch (change.entity) {
        case "ARTIFACTS":
          project.artifacts = <ArtifactSchema[]>change.entities;
          break;
        case "TRACES":
          project.traces = <TraceLinkSchema[]>change.entities;
          break;
        case "WARNINGS":
          break;
        case "TRACE_MATRICES":
          project.traceMatrices = <TraceMatrixSchema[]>change.entities;
          break;
        case "TYPES":
          project.artifactTypes = <ArtifactTypeSchema[]>change.entities;
          break;
        case "MEMBERS":
          project.members = <MembershipSchema[]>change.entities;
          break;
        case "ACTIVE_MEMBERS":
          project.members = <MembershipSchema[]>change.entities;
          break;
      }

      return project;
    }

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

    /**
     * Updates stored project information.
     *
     * @param change - The update change.
     * @param project - The project to update.
     */
    async function handleUpdateChange(
      change: ChangeSchema,
      project: ProjectSchema
    ) {
      const versionId = projectStore.versionId;

      switch (change.entity) {
        case "PROJECT":
          return projectStore.updateProject({
            name: project.name,
            description: project.description,
          });
        case "MEMBERS":
          //TODO: Non-trivial to retrieve the current `active` status of members.
          // Currently, active members are cleared when a new member is added.
          return membersStore.updateMembers(project.members, {
            entityType: "PROJECT",
            entityId: projectStore.projectId,
          });
        case "ACTIVE_MEMBERS":
          membersStore.setActiveMembers(project.members);
          break;
        case "VERSION":
          return getVersionApiStore.handleLoad(versionId);
        case "TYPES":
          return timStore.addOrUpdateArtifactTypes(project.artifactTypes);
        case "TRACE_MATRICES":
          return timStore.addOrUpdateTraceMatrices(project.traceMatrices);
        case "DOCUMENT":
          return await documentStore.updateDocuments(project.documents);
        case "ARTIFACTS":
          return artifactStore.addOrUpdateArtifacts(project.artifacts);
        case "TRACES":
          return traceStore.addOrUpdateTraceLinks(project.traces);
        case "WARNINGS":
          return warningApiStore.handleReload(versionId);
        case "JOBS":
          return jobApiStore.handleReload();
        case "LAYOUT":
          return documentStore.updateBaseLayout(project.layout);
        case "SUBTREES":
          return subtreeStore.initializeProject(project);
        case "MODELS":
          return projectStore.updateProject({ models: project.models });
        case "ATTRIBUTES":
          return attributesStore.updateAttributes(project.attributes || []);
        case "ATTRIBUTE_LAYOUTS":
          return attributesStore.updateAttributeLayouts(
            project.attributeLayouts || []
          );
      }
    }

    /**
     * Handles changes messages by updating affected parts of the app.
     *
     * @param frame - The message describing changes.
     */
    async function handleEntityChangeMessage(frame: Frame): Promise<void> {
      const message: ChangeMessageSchema = JSON.parse(frame.body);

      // Step - Iterate through message and delete entities.
      for (const change of message.changes) {
        if (change.action === ActionType.DELETE) {
          await handleDeleteChange(change);
        } else if (change.action === ActionType.UPDATE) {
          const project = createProjectSchema(change);

          await handleUpdateChange(change, project);
        } else {
          throw Error("Unable to handle action:" + change.action);
        }
      }
    }

    async function handleSubscribeVersion(
      projectId: string,
      versionId: string
    ): Promise<void> {
      if (!projectId || !versionId) {
        logStore.onDevError(
          "Received invalid project " + projectId + "or version id " + versionId
        );
        return;
      }
      if (stompApiStore.isConnected) {
        await clearProjectSubscriptions();
      }

      await stompApiStore.subscribeTo(
        fillEndpoint("projectTopic", { projectId }),
        handleEntityChangeMessage
      );
      await stompApiStore.subscribeTo(
        fillEndpoint("versionTopic", { versionId }),
        handleEntityChangeMessage
      );
    }

    /**
     * Change the current project subscribed to when the project changes.
     */
    projectStore.$subscribe((mutation) => {
      if (mutation.type === MutationType.direct) {
        if (mutation.events.key === "project") {
          const oldProject: ProjectSchema = mutation.events.oldValue;
          const newProject: ProjectSchema = mutation.events.newValue;
          const oldProjectVersion = oldProject.projectVersion?.versionId || "";
          const newProjectVersion = newProject.projectVersion?.versionId || "";

          if (newProjectVersion && oldProjectVersion !== newProjectVersion) {
            handleSubscribeVersion(
              newProject.projectId,
              newProjectVersion
            ).then();
          } else if (!newProjectVersion && oldProjectVersion) {
            // no project selected, clear subscriptions
            clearProjectSubscriptions().then();
          }
        }
      }
    });

    /**
     * Clears subscriptions to project and related versions.
     */
    async function clearProjectSubscriptions() {
      const channels: StompChannel[] = stompApiStore.channels;
      const projectSubscriptions = channels.filter((c) =>
        isProjectTopic(c.topic)
      );
      await stompApiStore.unsubscribe(projectSubscriptions);
    }

    return { handleSubscribeVersion };
  }
);

export default useNotificationApi(pinia);
