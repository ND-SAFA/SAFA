import { defineStore } from "pinia";

import {
  ArtifactMap,
  CreateProjectByJsonSchema,
  CreatorFilePanel,
  MembershipSchema,
  TimLinkProps,
  TimNodeProps,
  UploadPanelType,
} from "@/types";
import { buildEmptyPanel, buildProject } from "@/util";
import {
  identifierSaveStore,
  integrationsStore,
  orgStore,
  sessionStore,
  teamStore,
} from "@/hooks";
import { pinia } from "@/plugins";

/**
 * The save project store assists in creating new projects.
 */
export const useSaveProject = defineStore("saveProject", {
  state: () => ({
    uploadPanels: [buildEmptyPanel()] as CreatorFilePanel[],
    artifactMap: {} as ArtifactMap,
  }),
  getters: {
    /**
     * @return The current upload panel mode.
     */
    mode(): UploadPanelType {
      return this.uploadPanels[0]?.variant ?? "artifact";
    },
    /**
     * @return All artifact panels.
     */
    artifactPanels(): CreatorFilePanel[] {
      return this.uploadPanels.filter(({ variant }) => variant === "artifact");
    },
    /**
     * @return All trace panels.
     */
    tracePanels(): CreatorFilePanel[] {
      return this.uploadPanels.filter(({ variant }) => variant === "trace");
    },
    /**
     * @return All artifact types.
     */
    artifactTypes(): string[] {
      return this.artifactPanels.map(({ type }) => type);
    },
    /**
     * @return A project creation request with the uploaded data.
     */
    creationRequest(): CreateProjectByJsonSchema {
      const artifacts = this.artifactPanels
        .map(({ artifacts = [], type }) =>
          artifacts.map((artifact) => ({ ...artifact, type }))
        )
        .reduce((acc, cur) => [...acc, ...cur], []);
      const traces = this.tracePanels
        .map(({ traces = [] }) => traces)
        .reduce((acc, cur) => [...acc, ...cur], []);
      const requests = this.tracePanels
        .filter(({ isGenerated }) => isGenerated)
        .map(({ type, toType = "" }) => ({
          artifactLevels: [
            {
              source: type,
              target: toType,
            },
          ],
        }));
      const user: MembershipSchema = {
        id: "",
        email: sessionStore.userEmail,
        role: "OWNER",
        entityType: "PROJECT",
        entityId: "",
      };
      const project = buildProject({
        name: identifierSaveStore.editedIdentifier.name,
        description: identifierSaveStore.editedIdentifier.description,
        owner: user.email,
        members: [user],
        artifacts,
        traces,
      });

      return {
        orgId: orgStore.orgId,
        teamId: teamStore.teamId,
        project,
        requests,
      };
    },
    /**
     * @return The nodes to display on the graph.
     */
    graphNodes(): TimNodeProps[] {
      if (this.mode === "artifact" || this.mode === "trace") {
        return this.artifactPanels
          .filter(({ valid }) => valid)
          .map(({ type, artifacts = [] }) => ({
            artifactType: type,
            count: artifacts.length,
            hideActions: true,
          }));
      } else if (this.mode === "bulk") {
        return (
          this.uploadPanels[0]?.tim?.artifacts.map(({ type }) => ({
            artifactType: type,
            count: -1,
            hideActions: true,
          })) ?? []
        );
      } else if (this.mode === "github") {
        return [
          {
            artifactType:
              integrationsStore.gitHubConfig.artifactType || "GitHub Code",
            count: -1,
            hideActions: true,
          },
        ];
      } else if (this.mode === "jira") {
        return [
          {
            artifactType: "Jira Ticket",
            count: -1,
            hideActions: true,
          },
        ];
      } else {
        return [];
      }
    },
    /**
     * @return The edges to display on the graph.
     */
    graphEdges(): TimLinkProps[] {
      if (this.mode === "artifact" || this.mode === "trace") {
        return this.tracePanels
          .filter(({ valid }) => valid)
          .map(({ type, toType = "", traces = [], isGenerated }) => ({
            sourceType: type,
            targetType: toType,
            count: traces.length,
            generated: isGenerated,
            hideActions: true,
          }));
      } else if (this.mode === "bulk") {
        return (
          this.uploadPanels[0]?.tim?.traces.map(
            ({ sourceType, targetType }) => ({
              sourceType,
              targetType,
              count: -1,
              hideActions: true,
            })
          ) ?? []
        );
      } else {
        return [];
      }
    },
  },
  actions: {
    /**
     * Resets the created project state.
     */
    resetProject(): void {
      this.uploadPanels = [buildEmptyPanel()];
      this.artifactMap = {};
      identifierSaveStore.resetIdentifier(true);
    },
    /**
     * Adds a new creator panel.
     * @param variant - The type of panel to add.
     */
    addPanel(variant: UploadPanelType = "artifact"): void {
      this.uploadPanels.push(buildEmptyPanel(variant));
    },
    /**
     * Removes a creator panel.
     * @param variant - The type of panel to remove.
     * @param index - The panel index to remove.
     */
    removePanel(variant: UploadPanelType, index: number): void {
      this.uploadPanels = this.uploadPanels.filter((_, i) => i !== index);
    },
  },
});

export default useSaveProject(pinia);
