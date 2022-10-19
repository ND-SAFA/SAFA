import { defineStore } from "pinia";

import {
  ArtifactUploader,
  CreateProjectByJsonModel,
  MembershipModel,
  ProjectRole,
  TraceUploader,
} from "@/types";
import { createProject } from "@/util";
import sessionStore from "@/hooks/core/useSession";
import { pinia } from "@/plugins";

/**
 * The save project store assists in creating new projects.
 */
export const useSaveProject = defineStore("saveProject", {
  state: () => ({
    name: "",
    description: "",
  }),
  getters: {},
  actions: {
    /**
     * Resets the created project state.
     */
    resetProject(): void {
      this.name = "";
      this.description = "";
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
    ): CreateProjectByJsonModel {
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
      const user: MembershipModel = {
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
