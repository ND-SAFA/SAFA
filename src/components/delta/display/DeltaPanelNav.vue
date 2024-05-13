<template>
  <panel-card borderless title="Version Delta">
    <text-button
      v-if="deltaVersion && !!deltaVersion.versionId"
      block
      outlined
      label="Hide Delta View"
      icon="cancel"
      class="q-mb-md"
      @click="deltaApiStore.handleDisable()"
    />
    <select-input
      v-model="deltaVersion"
      :options="deltaApiStore.deltaVersions"
      :loading="deltaApiStore.loading"
      option-value="versionId"
      :option-label="getVersionName"
      label="Delta Version"
      hint="The version to view the delta between."
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the delta panel navigation.
 */
export default {
  name: "DeltaPanelNav",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { deltaApiStore, deltaStore } from "@/hooks";
import { TextButton, PanelCard, SelectInput } from "@/components/common";

const deltaVersion = computed({
  get() {
    return deltaStore.afterVersion;
  },
  set(newVersion) {
    deltaApiStore.handleCreate(newVersion);
  },
});

/**
 * Returns a version's name.
 * @param version - The version to name.
 * @return The version's name.
 */
function getVersionName(version: VersionSchema): string {
  return versionToString(version);
}
</script>
