<template>
  <text-button
    :loading="deltaApiStore.loading"
    label="Delta"
    data-cy="button-nav-delta"
    icon="view-delta"
    :disabled="deltaApiStore.deltaVersions.length === 0"
    @click="emit('click')"
  >
    <q-menu v-if="!deltaVersion">
      <typography variant="caption" x="2" y="1" value="Compare Against" />
      <q-list>
        <list-item
          v-for="version in deltaApiStore.deltaVersions"
          :key="version.versionId"
          v-close-popup
          clickable
          :title="getVersionName(version)"
          @click="deltaVersion = version"
        />
      </q-list>
    </q-menu>
  </text-button>
</template>

<script lang="ts">
/**
 * A button for opening delta view options.
 */
export default {
  name: "DeltaModeButton",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { deltaApiStore, deltaStore } from "@/hooks";
import { TextButton, ListItem, Typography } from "@/components/common";

const emit = defineEmits<{
  (e: "click"): void;
}>();

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
