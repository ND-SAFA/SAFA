<template>
  <v-menu>
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

    <v-list dense>
      <v-list-item>
        <v-btn text color="error" @click="handleLogout">Logout</v-btn>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import Vue from "vue";
import { sessionModule } from "@/store";
import { navigateTo, Routes } from "@/router";

export default Vue.extend({
  name: "account-dropdown",
  methods: {
    handleLogout(): void {
      sessionModule.logout().then(() => navigateTo(Routes.LOGIN_ACCOUNT));
    },
  },
});
</script>
