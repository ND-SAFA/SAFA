import { defineStore } from "pinia";

import {
  ArtifactMap,
  CreateProjectByJsonSchema,
  CreatorFilePanel,
  MembershipSchema,
  UploadPanelType,
} from "@/types";
import { buildProject } from "@/util";
import { orgStore, sessionStore, teamStore } from "@/hooks";
import { pinia } from "@/plugins";

const createEmptyPanel = (
  variant: UploadPanelType = "artifact"
): CreatorFilePanel => ({
  variant,
  name: "",
  type: "",
  open: true,
  valid: false,
  loading: false,
  ignoreErrors: false,
  itemNames: [],
  isGenerated: false,
  summarize: false,
  bulkFiles: [],
});

/**
 * The save project store assists in creating new projects.
 */
export const useSaveProject = defineStore("saveProject", {
  state: () => ({
    name: "",
    description: "",
    uploadPanels: [createEmptyPanel()] as CreatorFilePanel[],
    artifactMap: {} as ArtifactMap,
  }),
  getters: {
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
        .map(({ artifacts = [] }) => artifacts)
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
        name: this.name,
        description: this.description,
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
  },
  actions: {
    /**
     * Resets the created project state.
     */
    resetProject(): void {
      this.name = "";
      this.description = "";
      this.uploadPanels = [];
      this.artifactMap = {};
    },
    /**
     * Adds a new creator panel.
     * @param variant - The type of panel to add.
     */
    addPanel(variant: UploadPanelType = "artifact"): void {
      this.uploadPanels.push(createEmptyPanel(variant));
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
