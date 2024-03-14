import { defineStore } from "pinia";

import { computed, watch } from "vue";
import { IOHandlerCallback, TeamApiHook, TeamSchema } from "@/types";
import { logStore, orgStore, teamStore, useApi } from "@/hooks";
import { createTeam, deleteTeam, editTeam, getTeamProjects } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the teams API.
 */
export const useTeamApi = defineStore("teamApi", (): TeamApiHook => {
  const getTeamApi = useApi("getTeamApi");
  const saveTeamApi = useApi("saveTeamApi");
  const deleteTeamApi = useApi("deleteTeamApi");

  const saveTeamApiLoading = computed(() => saveTeamApi.loading);
  const deleteTeamApiLoading = computed(() => deleteTeamApi.loading);

  async function handleLoadState(): Promise<void> {
    if (!teamStore.team.id) return;

    await getTeamApi.handleRequest(async () => {
      teamStore.allProjects = await getTeamProjects(teamStore.team.id);
    });
  }

  async function handleSave(
    team: TeamSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await saveTeamApi.handleRequest(
      async () => {
        if (!team.id) {
          const createdTeam = await createTeam(orgStore.orgId, team);

          teamStore.addTeam(createdTeam);
          teamStore.team = createdTeam;
        } else {
          const editedTeam = await editTeam(orgStore.orgId, team);

          teamStore.addTeam(editedTeam);
          teamStore.team = editedTeam;
        }
      },
      {
        ...callbacks,
        success: `Team has been saved: ${team.name}`,
        error: `Unable to save team: ${team.name}`,
      }
    );
  }

  async function handleDelete(
    team: TeamSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    logStore.confirm(
      "Delete Team",
      `Are you sure you want to delete ${team.name}?`,
      async (isConfirmed) => {
        if (!isConfirmed) return;

        await deleteTeamApi.handleRequest(
          async () => {
            await deleteTeam(orgStore.orgId, team);

            teamStore.removeTeam(team);
          },
          {
            ...callbacks,
            success: `Team has been deleted: ${team.name}`,
            error: `Unable to delete team: ${team.name}`,
          }
        );
      }
    );
  }

  // Reload the current team's data when the team changes.
  watch(
    () => teamStore.team,
    () => handleLoadState()
  );

  return {
    saveTeamApiLoading,
    deleteTeamApiLoading,
    handleLoadState,
    handleSave,
    handleDelete,
  };
});

export default useTeamApi(pinia);
