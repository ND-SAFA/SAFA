<template>
  <generic-stepper-list-step
    title="GitHub Installations"
    :item-count="installations.length"
    :loading="loading"
    empty-message="There are no installations."
  >
    <template slot="items">
      <template v-for="installation in installations">
        <v-list-item
          :key="installation.id"
          @click="handleInstallationSelect(installation)"
        >
          <v-list-item-content>
            <v-list-item-title
              v-text="installation.name || installation.app_slug"
            />
            <v-list-item-subtitle v-text="installation.url" />
          </v-list-item-content>
        </v-list-item>
      </template>
    </template>
  </generic-stepper-list-step>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GitHubInstallation } from "@/types";
import { GenericStepperListStep } from "@/components/common";

/**
 * Allows for selecting a GitHub installation.
 *
 * @emits `select` (GitHubInstallation) - On site selection.
 */
export default Vue.extend({
  name: "GitHubInstallationSelector",
  components: {
    GenericStepperListStep,
  },
  props: {
    installations: {
      type: Array as PropType<GitHubInstallation[]>,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
    },
  },
  methods: {
    /**
     * Handles a click to select an installation.
     * @param installation - The installation to select.
     */
    handleInstallationSelect(installation: GitHubInstallation) {
      this.$emit("select", installation);
    },
  },
});
</script>
