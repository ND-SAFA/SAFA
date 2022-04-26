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
          <template v-for="upload in uploads">
            <v-expansion-panel :key="upload.id">
              <v-expansion-panel-header>
                <v-row no-gutters>
                  <v-col cols="4"> {{ upload.name }} </v-col>
                  <v-col cols="8" class="text--secondary">
                    <span v-if="isCompleted(upload.status)">
                      {{ getCompletedText(upload.completedAt) }}
                    </span>
                    <v-row v-else no-gutters justify="right">
                      <v-col cols="4">
                        Upload Progress: {{ upload.currentProgress }}%
                      </v-col>
                      <v-col cols="4">
                        {{ getUpdatedText(upload.lastUpdatedAt) }}
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
                <template v-slot:actions>
                  <v-chip :color="getStatusColor(upload.status)">
                    {{ upload.status }}
                  </v-chip>
                </template>
              </v-expansion-panel-header>

              <v-expansion-panel-content>
                <v-list>
                  <template v-for="(step, idx) in upload.steps">
                    <v-list-item :key="step.id">
                      <v-list-item-content>
                        <v-list-item-title>
                          {{ step.message }}
                        </v-list-item-title>
                      </v-list-item-content>
                      <v-list-item-action>
                        <v-list-item-action-text>
                          {{ step.progress }}% |
                          {{ stringifyTimestamp(step.timestamp) }}
                        </v-list-item-action-text>
                      </v-list-item-action>
                    </v-list-item>

                    <v-divider :key="idx" />
                  </template>
                </v-list>

                <v-btn color="primary" :disabled="!isCompleted(upload.status)">
                  View Project
                </v-btn>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </template>
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
  data() {
    return {
      uploads: [
        {
          id: "1",
          name: "Project 1",
          status: "In Progress",
          startedAt: "2022-04-27T10:00:00.000Z",
          lastUpdatedAt: "2022-04-27T10:10:00.000Z",
          currentProgress: 50,
          completedAt: null,
          steps: [
            {
              id: "3",
              message:
                "Trace links have been created. Beginning trace link generation.",
              timestamp: "2022-04-27T10:10:00.000Z",
              progress: 50,
            },
            {
              id: "2",
              message:
                "Artifacts have been created. Beginning to create trace links.",
              timestamp: "2022-04-27T10:05:00.000Z",
              progress: 30,
            },
            {
              id: "1",
              message:
                "Import has been submitted. Beginning to create artifacts.",
              timestamp: "2022-04-27T10:00:00.000Z",
              progress: 0,
            },
          ],
        },
        {
          id: "2",
          name: "Project 2",
          status: "Completed",
          startedAt: "2022-04-27T10:00:00.000Z",
          lastUpdatedAt: "2022-04-27T10:15:00.000Z",
          completedAt: "2022-04-27T10:15:00.000Z",
          currentProgress: 100,
          steps: [
            {
              id: "5",
              message: "Project has been created.",
              timestamp: "2022-04-27T10:15:00.000Z",
              progress: 100,
            },
            {
              id: "4",
              message: "Trace links have been generated.",
              timestamp: "2022-04-27T10:15:00.000Z",
              progress: 75,
            },
            {
              id: "3",
              message:
                "Trace links have been created. Beginning trace link generation.",
              timestamp: "2022-04-27T10:10:00.000Z",
              progress: 50,
            },
            {
              id: "2",
              message:
                "Artifacts have been created. Beginning to create trace links.",
              timestamp: "2022-04-27T10:05:00.000Z",
              progress: 30,
            },
            {
              id: "1",
              message:
                "Import has been submitted. Beginning to create artifacts.",
              timestamp: "2022-04-27T10:00:00.000Z",
              progress: 0,
            },
          ],
        },
      ],
    };
  },
  methods: {
    /**
     * Goes back to the artifact page.
     */
    handleGoBack() {
      navigateBack();
    },
    isCompleted(status: string) {
      return status === "Completed";
    },
    getUpdatedText(timestamp: string) {
      return "Last Update: 10:00 AM, Apr 27, 2022";
    },
    getCompletedText(timestamp: string) {
      return "Upload Completed: 10:00 AM, Apr 27, 2022";
    },
    stringifyTimestamp(timestamp: string) {
      return "10:00 AM, Apr 27, 2022";
    },
    getStatusColor(status: string) {
      switch (status) {
        case "Completed":
          return "#64b5f6";
        case "In Progress":
          return "#81c784";
        default:
          return "";
      }
    },
  },
});
</script>
