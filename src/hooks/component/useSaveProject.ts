import { defineStore } from "pinia";

import {
  ArtifactMap,
  CreateProjectByJsonSchema,
  CreatorFilePanel,
  MembershipSchema,
} from "@/types";
import { buildProject } from "@/util";
import { orgStore, sessionStore, teamStore } from "@/hooks";
import { pinia } from "@/plugins";

const createEmptyPanel = (variant: "artifact" | "trace"): CreatorFilePanel => ({
  variant,
  name: "",
  type: "",
  open: true,
  valid: false,
  loading: false,
  ignoreErrors: false,
  itemNames: [],
  isGenerated: false,
  generateMethod: undefined,
});

/**
 * The save project store assists in creating new projects.
 */
export const useSaveProject = defineStore("saveProject", {
  state: () => ({
    name: "",
    description: "",
    artifactPanels: [createEmptyPanel("artifact")] as CreatorFilePanel[],
    tracePanels: [createEmptyPanel("trace")] as CreatorFilePanel[],
    artifactMap: {} as ArtifactMap,
  }),
  getters: {
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
        .map(({ type, toType = "", generateMethod }) => ({
          artifactLevels: [
            {
              source: type,
              target: toType,
            },
          ],
          method: generateMethod,
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
      this.artifactPanels = [createEmptyPanel("artifact")];
      this.tracePanels = [createEmptyPanel("trace")];
      this.artifactMap = {};
    },
    /**
     * Adds a new creator panel.
     * @param variant - The type of panel to add.
     */
    addPanel(variant: "artifact" | "trace"): void {
      if (variant === "artifact") {
        this.artifactPanels.push(createEmptyPanel("artifact"));
      } else {
        this.tracePanels.push(createEmptyPanel("trace"));
      }
    },
    /**
     * Removes a creator panel.
     * @param variant - The type of panel to remove.
     * @param index - The panel index to remove.
     */
    removePanel(variant: "artifact" | "trace", index: number): void {
      if (variant === "artifact") {
        this.artifactPanels = this.artifactPanels.filter((_, i) => i !== index);
      } else {
        this.tracePanels = this.tracePanels.filter((_, i) => i !== index);
      }
    },
  },
});

export default useSaveProject(pinia);
