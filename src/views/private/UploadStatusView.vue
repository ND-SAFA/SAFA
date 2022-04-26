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
                    <v-row v-if="isCancelled(upload.status)" no-gutters>
                      <v-col cols="4"> Upload Cancelled </v-col>
                      <v-col cols="4">
                        {{ getUpdatedText(upload.lastUpdatedAt) }}
                      </v-col>
                    </v-row>
                    <span v-else-if="isCompleted(upload.status)">
                      {{ getCompletedText(upload.completedAt) }}
                    </span>
                    <v-row v-else no-gutters>
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
                <v-stepper
                  alt-labels
                  class="elevation-0"
                  v-model="upload.currentStep"
                >
                  <v-stepper-header>
                    <v-stepper-step step="1">
                      <span style="width: 130px">
                        {{
                          upload.currentStep !== 1
                            ? "Project Initialized"
                            : `Initializing Project${getEllipse()}`
                        }}
                      </span>
                    </v-stepper-step>
                    <v-divider />
                    <v-stepper-step step="2">
                      <span style="width: 130px">
                        {{
                          upload.currentStep !== 2
                            ? "Artifacts Imported"
                            : `Importing Artifacts${getEllipse()}`
                        }}
                      </span>
                    </v-stepper-step>
                    <v-divider />
                    <v-stepper-step step="3">
                      <span style="width: 130px">
                        {{
                          upload.currentStep !== 3
                            ? "Traces Imported"
                            : `Importing Traces${getEllipse()}`
                        }}
                      </span>
                    </v-stepper-step>
                    <v-divider />
                    <v-stepper-step step="4">
                      <span style="width: 130px">
                        {{
                          upload.currentStep !== 4
                            ? "Traces Generated"
                            : `Generating Traces${getEllipse()}`
                        }}
                      </span>
                    </v-stepper-step>
                    <v-divider />
                    <v-stepper-step step="5"> Project Imported </v-stepper-step>
                  </v-stepper-header>
                </v-stepper>

                <div class="d-flex">
                  <v-btn
                    v-if="isInProgress(upload.status)"
                    color="error"
                    class="mr-1"
                  >
                    Cancel Upload
                  </v-btn>
                  <v-btn
                    color="primary"
                    :disabled="!isCompleted(upload.status)"
                  >
                    View Project
                  </v-btn>
                </div>
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
import { setTimeout } from "timers";

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
      timer: undefined as ReturnType<typeof setTimeout> | undefined,
      ellipse: "...",
      uploads: [
        {
          id: "1",
          name: "Project 1",
          status: "In Progress",
          startedAt: "2022-04-27T10:00:00.000Z",
          lastUpdatedAt: "2022-04-27T10:10:00.000Z",
          completedAt: null,
          currentProgress: 50,
          currentStep: 3,
        },
        {
          id: "2",
          name: "Project 2",
          status: "Completed",
          startedAt: "2022-04-27T10:00:00.000Z",
          lastUpdatedAt: "2022-04-27T10:15:00.000Z",
          completedAt: "2022-04-27T10:15:00.000Z",
          currentProgress: 100,
          currentStep: 5,
        },
        {
          id: "3",
          name: "Project 3",
          status: "Cancelled",
          startedAt: "2022-04-27T10:00:00.000Z",
          lastUpdatedAt: "2022-04-27T10:15:00.000Z",
          completedAt: null,
          currentProgress: 50,
          currentStep: 3,
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
    isInProgress(status: string) {
      return status === "In Progress";
    },
    isCancelled(status: string) {
      return status === "Cancelled";
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
          return "#EEBC3D";
        case "Cancelled":
          return "#e57373";
        default:
          return "";
      }
    },
    getEllipse(): string {
      // if (!this.timer) {
      //   this.timer = setTimeout(() => {
      //     if (this.ellipse.length === 3) {
      //       this.ellipse = ".";
      //     } else {
      //       this.ellipse += ".";
      //     }
      //
      //     if (!this.timer) return;
      //
      //     clearTimeout(this.timer);
      //   }, 1000);
      // }

      return this.ellipse;
    },
  },
});
</script>
