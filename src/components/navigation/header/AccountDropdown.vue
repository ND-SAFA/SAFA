<template>
  <v-menu rounded min-width="200px" bottom offset-y id="my-account">
    <template v-slot:activator="{ on: menuOn, attrs }">
      <v-tooltip bottom>
        <template v-slot:activator="{ on: tooltipOn }">
          <v-btn
            icon
            v-on="{ ...tooltipOn, ...menuOn }"
            v-bind="attrs"
            data-cy="account-dropdown"
          >
            <v-avatar>
              <v-icon color="secondary" style="font-size: 48px">
                mdi-account-circle
              </v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <span>My Account</span>
      </v-tooltip>
    </template>

    <v-card>
      <v-list-item-content class="justify-center">
        <div class="text-center">
          <v-avatar>
            <v-icon color="secondary" style="font-size: 48px">
              mdi-account-circle
            </v-icon>
          </v-avatar>
          <typography
            el="div"
            align="center"
            variant="subtitle"
            :value="userName"
          />
          <typography
            el="div"
            align="center"
            variant="caption"
            :value="userEmail"
          />
          <v-divider class="my-3" />
          <v-btn text rounded @click="handleFeedback">Send Feedback</v-btn>
          <br />
          <v-btn text rounded @click="handleEditAccount">Edit Account</v-btn>
          <v-divider class="my-3"></v-divider>
          <v-btn
            text
            rounded
            color="error"
            @click="handleLogout"
            data-cy="button-logout"
          >
            Logout
          </v-btn>
        </div>
      </v-list-item-content>
    </v-card>
  </v-menu>
</template>

<script lang="ts">
import Vue from "vue";
import { sessionStore } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import { handleLogout } from "@/api";
import { Typography } from "@/components/common";

export default Vue.extend({
  name: "AccountDropdown",
  components: { Typography },
  computed: {
    /**
     * @return The current user's email.
     */
    userEmail() {
      return sessionStore.userEmail;
    },
    /**
     * @return The current user's name.
     */
    userName() {
      return "SAFA User";
    },
  },
  methods: {
    /**
     * Routes the user to the feedback page.
     */
    handleFeedback(): void {
      window.open(
        "https://www.notion.so/nd-safa/b73d1a8bfe0345f8b4d72daa1ceaf934?v=6e5d2439907a428fa1db2671a5eaa0b6"
      );
    },
    /**
     * Logs the user out.
     */
    handleLogout(): void {
      handleLogout();
    },
    /**
     * Navigates to the account editing page.
     */
    handleEditAccount(): void {
      navigateTo(Routes.ACCOUNT);
    },
  },
});
</script>
