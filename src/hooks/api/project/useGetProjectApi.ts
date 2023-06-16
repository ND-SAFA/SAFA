import { defineStore } from "pinia";

import { computed, ref } from "vue";
import { IdentifierSchema, IOHandlerCallback } from "@/types";
import { removeMatches } from "@/util";
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

  const allProjects = ref<IdentifierSchema[]>([]);

  const unloadedProjects = computed(() =>
    allProjects.value.filter(
      ({ projectId }) => projectId !== projectStore.projectId
    )
  );

  const loading = computed(() => getProjectApi.loading);

  const currentProject = computed({
    get: () => (projectStore.projectId ? projectStore.project : undefined),
    set(identifier: IdentifierSchema | undefined) {
      if (!identifier) return;

      getVersionApiStore.handleLoadCurrent(identifier);
    },
  });

  /**
   * Adds or replaces a project in the project list.
   *
   * @param project - The project to add.
   */
  function addProject(project: IdentifierSchema): void {
    allProjects.value = [
      project,
      ...removeMatches(allProjects.value, "projectId", [project.projectId]),
    ];
  }

  /**
   * Stores all projects for the current user.
   *
   * @param callbacks - The callbacks to call after the action.
   */
  async function handleReload(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    if (!sessionStore.doesSessionExist) {
      callbacks.onSuccess?.();
      return;
    }

    await getProjectApi.handleRequest(
      async () => {
        allProjects.value = await getProjects();
      },
      callbacks,
      { error: "Unable to load your projects." }
    );
  }

  /**
   * Loads the last stored project.
   */
  async function handleLoadRecent(): Promise<void> {
    if (!sessionStore.doesSessionExist) return;

    let versionId = getParam(QueryParams.VERSION);

    if (!versionId) {
      if (allProjects.value.length > 0) {
        versionId = (await getCurrentVersion(allProjects.value[0].projectId))
          .versionId;
      }
    }
    if (typeof versionId === "string") {
      await getVersionApiStore.handleLoad(versionId).catch(() => {
        navigateTo(Routes.HOME);
      });
    } else {
      await navigateTo(Routes.HOME);
    }
  }

  return {
    loading,
    allProjects,
    unloadedProjects,
    currentProject,
    addProject,
    handleReload,
    handleLoadRecent,
  };
});

export default useGetProjectApi(pinia);
