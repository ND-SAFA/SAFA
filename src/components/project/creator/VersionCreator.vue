<template>
  <modal
    :title="`Current Version: ${versionName}`"
    :open="props.open"
    :loading="createVersionApiStore.loading"
    data-cy="modal-version-create"
    @close="emit('close')"
  >
    <flex-box column align="center">
      <text-button
        text
        :label="`New Major Version: ${nextVersion('major')}`"
        color="primary"
        data-cy="button-create-major-version"
        @click="() => handleClick('major')"
      />
      <text-button
        text
        :label="`New Minor Version: ${nextVersion('minor')}`"
        color="primary"
        data-cy="button-create-minor-version"
        @click="() => handleClick('minor')"
      />
      <text-button
        text
        :label="`New Revision: ${nextVersion('revision')}`"
        color="primary"
        data-cy="button-create-revision-version"
        @click="() => handleClick('revision')"
      />
    </flex-box>
  </modal>
</template>

<script lang="ts">
/**
 * A modal for creating new versions.
 */
export default {
  name: "VersionCreator",
};
</script>

<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { IdentifierSchema, VersionSchema, VersionType } from "@/types";
import { versionToString } from "@/util";
import { createVersionApiStore } from "@/hooks";
import { getCurrentVersion } from "@/api";
import { Modal, TextButton, FlexBox } from "@/components/common";

const props = defineProps<{
  open: boolean;
  project?: IdentifierSchema;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "create", version: VersionSchema): void;
}>();

const currentVersion = ref<VersionSchema | undefined>();

const versionName = computed(() => versionToString(currentVersion.value));

/**
 * Returns the next version name.
 * @param type - The type of new version.
 */
function nextVersion(type: VersionType): string {
  if (currentVersion.value === undefined) {
    return "X.X.X";
  }

  const { majorVersion, minorVersion, revision } = currentVersion.value;

  switch (type) {
    case "major":
      return `${majorVersion + 1}.0.0`;
    case "minor":
      return `${majorVersion}.${minorVersion + 1}.0`;
    case "revision":
      return `${majorVersion}.${minorVersion}.${revision + 1}`;
  }
}

/**
 * Creates a new version.
 * @param versionType - The version type to create.
 */
function handleClick(versionType: VersionType) {
  if (!props.project) return;

  createVersionApiStore.handleCreateVersion(
    props.project.projectId,
    versionType,
    {
      onSuccess: (version) => emit("create", version),
    }
  );
}

watch(
  () => props.open,
  (open) => {
    if (!open || !props.project) return;

    getCurrentVersion(props.project.projectId).then(
      (version) => (currentVersion.value = version)
    );
  }
);
</script>
