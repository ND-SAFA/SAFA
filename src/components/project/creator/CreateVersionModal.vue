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
  name: "CreateVersionModal",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { CreateVersionModalProps, VersionSchema, VersionType } from "@/types";
import { versionToString } from "@/util";
import { createVersionApiStore, projectStore } from "@/hooks";
import { Modal, TextButton, FlexBox } from "@/components/common";

const props = defineProps<CreateVersionModalProps>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "create", version: VersionSchema): void;
}>();

const versionName = computed(() => versionToString(projectStore.version));

/**
 * Returns the next version name.
 * @param type - The type of new version.
 */
function nextVersion(type: VersionType): string {
  if (projectStore.version === undefined) {
    return "X.X.X";
  }

  const { majorVersion, minorVersion, revision } = projectStore.allVersions[0];

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

  createVersionApiStore.handleCreate(props.project.projectId, versionType, {
    onSuccess: (version) => emit("create", version),
  });
}
</script>
