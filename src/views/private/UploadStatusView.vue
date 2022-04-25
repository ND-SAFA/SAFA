<template>
  <private-page>
    <template v-slot:page>
      <v-container>
        <h1 class="text-h4">Current Uploads</h1>
        <v-divider />
        <p class="text-body-1 mt-2 mb-3">
          Select a project below to see more detailed updates on the import
          status.
        </p>
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>
              <v-row no-gutters>
                <v-col cols="4"> Project 1 </v-col>
                <v-col cols="8" class="text--secondary">
                  <v-row no-gutters justify="right">
                    <v-col cols="4"> Upload Started: Apr 27, 2022 </v-col>
                    <v-col cols="4"> Last Status Update: 10:35 AM </v-col>
                  </v-row>
                </v-col>
              </v-row>
              <template v-slot:actions>
                <v-chip color="#81c784">In Progress</v-chip>
              </template>
            </v-expansion-panel-header>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-header>
              <v-row no-gutters>
                <v-col cols="4"> Project 2 </v-col>
                <v-col cols="8" class="text--secondary">
                  <v-row no-gutters justify="right">
                    <v-col cols="4"> Upload Completed: Apr 27, 2022 </v-col>
                  </v-row>
                </v-col>
              </v-row>
              <template v-slot:actions>
                <v-chip color="#64b5f6">Completed</v-chip>
              </template>
            </v-expansion-panel-header>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateBack } from "@/router";
import { PrivatePage } from "@/components";

/**
 * Displays project settings.
 */
export default Vue.extend({
  name: "UploadStatusView",
  components: {
    PrivatePage,
  },
  methods: {
    /**
     * Goes back to the artifact page.
     */
    handleGoBack() {
      navigateBack();
    },
  },
});
</script>
