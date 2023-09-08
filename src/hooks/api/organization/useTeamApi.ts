import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, TeamApiHook, TeamSchema } from "@/types";
import { removeMatches } from "@/util";
import { logStore, orgStore, teamStore, useApi } from "@/hooks";
import { createTeam, deleteTeam, editTeam } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the teams API.
 */
export const useTeamApi = defineStore("teamApi", (): TeamApiHook => {
  const saveTeamApi = useApi("saveTeamApi");
  const deleteTeamApi = useApi("deleteTeamApi");

  const saveTeamApiLoading = computed(() => saveTeamApi.loading);
  const deleteTeamApiLoading = computed(() => deleteTeamApi.loading);

  async function handleSave(
    team: TeamSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await saveTeamApi.handleRequest(
      async () => {
        if (!team.id) {
          const createdTeam = await createTeam(orgStore.orgId, team);

          orgStore.org.teams.push(createdTeam);
          teamStore.team = createdTeam;
        } else {
          const editedTeam = await editTeam(orgStore.orgId, team);

          orgStore.org.teams = [
            ...removeMatches(orgStore.org.teams, "id", [team.id]),
            editedTeam,
          ];
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

            orgStore.org.teams = removeMatches(orgStore.org.teams, "id", [
              team.id,
            ]);

            if (teamStore.teamId !== team.id) return;

            // Clear the current team if it was deleted.
            teamStore.$reset();
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

  return {
    saveTeamApiLoading,
    deleteTeamApiLoading,
    handleSave,
    handleDelete,
  };
});

export default useTeamApi(pinia);
