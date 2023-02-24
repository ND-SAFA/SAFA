import { defineStore } from "pinia";

import {
  ArtifactMap,
  ArtifactUploader,
  CreateProjectByJsonSchema,
  CreatorFilePanel,
  MembershipSchema,
  ModelType,
  ProjectRole,
  TraceUploader,
} from "@/types";
import { createProject } from "@/util";
import sessionStore from "@/hooks/core/useSession";
import { pinia } from "@/plugins";

const createEmptyPanel = (variant: "artifact" | "trace"): CreatorFilePanel => ({
  variant,
  name: "",
  type: "",
  open: true,
  ignoreErrors: false,
  itemNames: [],
  isGenerated: false,
  generateMethod: ModelType.NLBert,
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
  getters: {},
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
    /**
     * Creates a project creation request from uploaded data.
     *
     * @param artifactUploader - The uploaded artifacts.
     * @param traceUploader - The uploaded trace links.
     * @return The request to create this project.
     */
    getCreationRequest(
      artifactUploader: ArtifactUploader,
      traceUploader: TraceUploader
    ): CreateProjectByJsonSchema {
      const artifacts = artifactUploader.panels
        .map(({ projectFile }) => projectFile.artifacts || [])
        .reduce((acc, cur) => [...acc, ...cur], []);
      const traces = traceUploader.panels
        .map(({ projectFile }) => projectFile.traces || [])
        .reduce((acc, cur) => [...acc, ...cur], []);
      const requests = traceUploader.panels
        .filter(({ projectFile }) => projectFile.isGenerated)
        .map(({ projectFile }) => ({
          artifactLevels: [
            {
              source: projectFile.sourceId,
              target: projectFile.targetId,
            },
          ],
          method: projectFile.method,
        }));
      const user: MembershipSchema = {
        projectMembershipId: "",
        email: sessionStore.userEmail,
        role: ProjectRole.OWNER,
      };
      const project = createProject({
        name: this.name,
        description: this.description,
        owner: user.email,
        members: [user],
        artifacts,
        traces,
      });

      return { project, requests };
    },
  },
});

export default useSaveProject(pinia);
