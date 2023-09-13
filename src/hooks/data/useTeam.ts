import { defineStore } from "pinia";

import { TeamSchema } from "@/types";
import { buildTeam, removeMatches } from "@/util";
import { orgStore, permissionStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * A store for managing the state of the user's current team.
 */
export const useTeam = defineStore("team", {
  state: () => ({
    /**
     * The currently loaded team.
     */
    team: buildTeam(),
  }),
  getters: {
    /**
     * @return The current team id.
     */
    teamId(): string {
      return this.team.id;
    },
    /**
     * @return The current organization's teams.
     */
    allTeams(): TeamSchema[] {
      return orgStore.org.teams;
    },
    /**
     * @return The current organization's teams that allow the current user
     * to create a project.
     */
    teamsWithCreateProject(): TeamSchema[] {
      return orgStore.org.teams.filter((team) =>
        permissionStore.isAllowed("team.create_projects", team)
      );
    },
  },
  actions: {
    /**
     * Adds a team to the list of all teams.
     * @param team - The team to add.
     */
    addTeam(team: TeamSchema): void {
      orgStore.org.teams = [
        team,
        ...removeMatches(this.allTeams, "id", [team.id]),
      ];
    },
    /**
     * Removes a team to the list of all teams.
     * @param team - The team to remove.
     */
    removeTeam(team: TeamSchema): void {
      orgStore.org.teams = removeMatches(this.allTeams, "id", [team.id]);

      if (team.id === this.teamId) {
        this.team = this.allTeams[0] || buildTeam();
      }
    },
  },
});

export default useTeam(pinia);
