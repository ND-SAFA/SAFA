<template>
  <text-button
    :loading="loading"
    label="Delta"
    data-cy="button-nav-delta"
    icon="view-delta"
    @click="emit('click')"
  >
    <q-menu v-if="!deltaVersion">
      <typography variant="caption" x="2" y="1" value="Compare Against" />
      <q-list>
        <list-item
          v-for="version in versions"
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
import { computed, onMounted, ref, watch } from "vue";
import { VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { deltaStore, projectStore } from "@/hooks";
import { getProjectVersions, handleSetProjectDelta } from "@/api";
import { TextButton, ListItem } from "@/components/common";
import Typography from "@/components/common/display/content/Typography.vue";

const emit = defineEmits<{
  (e: "click"): void;
}>();

const loading = ref(false);
const versions = ref<VersionSchema[]>([]);

const deltaVersion = computed({
  get() {
    return deltaStore.afterVersion;
  },
  set(newVersion) {
    if (!newVersion || !projectStore.version) return;

    loading.value = true;

    handleSetProjectDelta(projectStore.version, newVersion, () => {
      loading.value = false;
    });
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

/**
 * Loads the versions of the current project.
 */
async function loadVersions(): Promise<void> {
  const projectId = projectStore.projectId;

  versions.value = projectId
    ? (await getProjectVersions(projectId)).filter(
        ({ versionId }) => versionId !== projectStore.version?.versionId
      )
    : [];
}

watch(
  () => projectStore.projectId,
  () => loadVersions()
);

onMounted(() => loadVersions());
</script>
