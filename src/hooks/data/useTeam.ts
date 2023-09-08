import { defineStore } from "pinia";

import { buildTeam } from "@/util";
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
  },
  actions: {},
});

export default useTeam(pinia);
