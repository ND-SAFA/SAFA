<template>
  <v-menu rounded min-width="200px" bottom offset-y>
    <template v-slot:activator="{ on: menuOn, attrs }">
      <v-tooltip bottom>
        <template v-slot:activator="{ on: tooltipOn }">
          <v-btn icon v-on="{ ...tooltipOn, ...menuOn }" v-bind="attrs">
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
        <div class="mx-auto text-center">
          <v-avatar>
            <v-icon color="secondary" style="font-size: 48px">
              mdi-account-circle
            </v-icon>
          </v-avatar>
          <h3 class="text-h6">{{ userName }}</h3>
          <p class="text-caption mx-1">{{ userEmail }}</p>
          <v-divider class="my-3"></v-divider>
          <v-btn text rounded @click="handleEditAccount">Edit Account</v-btn>
          <v-divider class="my-3"></v-divider>
          <v-btn text rounded color="error" @click="handleLogout">Logout</v-btn>
        </div>
      </v-list-item-content>
    </v-card>
  </v-menu>
</template>

<script lang="ts">
import Vue from "vue";
import { logout } from "@/api";
import { logModule, sessionModule } from "@/store";

export default Vue.extend({
  name: "account-dropdown",
  computed: {
    userEmail() {
      return sessionModule.userEmail;
    },
    userName() {
      return "Demo User";
    },
  },
  methods: {
    handleLogout(): void {
      logout();
    },
    handleEditAccount(): void {
      logModule.onInfo("Account editing is not yet available");
    },
  },
});
</script>
