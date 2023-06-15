import { defineStore } from "pinia";

import { computed, onMounted } from "vue";
import { IdentifierSchema, IOHandlerCallback } from "@/types";
import {
  getVersionApiStore,
  projectStore,
  sessionStore,
  useApi,
} from "@/hooks";
import { getParam, navigateTo, QueryParams, Routes } from "@/router";
import { getCurrentVersion, getProjects } from "@/api";
import { pinia } from "@/plugins";

export const useGetProjectApi = defineStore("getProjectApi", () => {
  const getProjectApi = useApi("getProjectApi");

  const loading = computed(() => getProjectApi.loading);
  const allProjects = computed(() => projectStore.allProjects);

  const currentProject = computed({
    get: () => (projectStore.projectId ? projectStore.project : undefined),
    set(identifier: IdentifierSchema | undefined) {
      if (!identifier) return;

      getVersionApiStore.handleLoadCurrentVersion(identifier);
    },
  });

  /**
   * Stores all projects for the current user.
   *
   * @param callbacks - The callbacks to call after the action.
   */
  async function handleGetProjects(
    callbacks: IOHandlerCallback
  ): Promise<void> {
    if (!sessionStore.doesSessionExist) {
      callbacks.onSuccess?.();
      return;
    }

    await getProjectApi.handleRequest(
      async () => {
        projectStore.allProjects = await getProjects();
      },
      callbacks,
      { error: "Unable to load your projects." }
    );
  }

  /**
   * Loads the last stored project.
   */
  async function handleLoadLastProject(): Promise<void> {
    if (!sessionStore.doesSessionExist) return;

    let versionId = getParam(QueryParams.VERSION);

    if (!versionId) {
      const projects = projectStore.allProjects;

      if (projects.length > 0) {
        versionId = (await getCurrentVersion(projects[0].projectId)).versionId;
      }
    }
    if (typeof versionId === "string") {
      await getVersionApiStore.handleLoadVersion(versionId).catch(() => {
        navigateTo(Routes.HOME);
      });
    } else {
      await navigateTo(Routes.HOME);
    }
  }

  onMounted(() => handleGetProjects({}));

  return {
    loading,
    allProjects,
    currentProject,
    handleGetProjects,
    handleLoadLastProject,
  };
});

export default useGetProjectApi(pinia);
