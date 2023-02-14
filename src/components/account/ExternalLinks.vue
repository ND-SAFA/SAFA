<template>
  <panel-card>
    <typography variant="subtitle" el="h2" value="SAFA Documentation" />
    <v-divider class="mb-2" />
    <flex-box full-width justify="center" column>
      <v-btn text @click="handleFeedback">Send Feedback</v-btn>
      <v-btn text @click="handleWalkthrough">Walkthrough</v-btn>
      <v-btn text @click="handleChangelog">Recent Changes</v-btn>
    </flex-box>
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { PanelCard, FlexBox, Typography } from "@/components/common";

/**
 * Provides links to external documentation.
 */
export default defineComponent({
  name: "ExternalLinks",
  components: {
    PanelCard,
    FlexBox,
    Typography,
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
     * Routes the user to the walkthrough page.
     */
    handleWalkthrough(): void {
      window.open(
        "https://www.notion.so/nd-safa/8dc14ae706074b099928afe13df39448?v=5b5e744919f84178bac1c96f5a5a92ba"
      );
    },
    /**
     * Routes the user to the walkthrough page.
     */
    handleChangelog(): void {
      window.open(
        "https://www.notion.so/nd-safa/5155dc357f534eb49f8071a03ce3ae32?v=74f671825a1b4d048909843740c003f1"
      );
    },
  },
});
</script>
