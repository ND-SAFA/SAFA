<template>
  <modal
    :title="`Current Version: ${versionName}`"
    :is-open="props.isOpen"
    :is-loading="isLoading"
    data-cy="modal-version-create"
    @close="emit('close')"
  >
    <flex-box column align="center">
      <text-button
        text
        color="primary"
        data-cy="button-create-major-version"
        @click="() => handleClick('major')"
      >
        New Major Version: {{ nextVersion("major") }}
      </text-button>
      <text-button
        text
        color="primary"
        data-cy="button-create-minor-version"
        @click="() => handleClick('minor')"
      >
        New Minor Version: {{ nextVersion("minor") }}
      </text-button>
      <text-button
        text
        color="primary"
        data-cy="button-create-revision-version"
        @click="() => handleClick('revision')"
      >
        New Revision: {{ nextVersion("revision") }}
      </text-button>
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
import { ref, defineProps, watch, defineEmits, computed } from "vue";
import { IdentifierSchema, VersionSchema, VersionType } from "@/types";
import { versionToString } from "@/util";
import { getCurrentVersion, handleCreateVersion } from "@/api";
import { Modal, TextButton } from "@/components/common";
import FlexBox from "@/components/common/layout/FlexBox.vue";

const props = defineProps<{
  isOpen: boolean;
  project?: IdentifierSchema;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "create", version: VersionSchema): void;
}>();

const isLoading = ref(false);
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
      return `${majorVersion + 1}.${minorVersion}.${revision}`;
    case "minor":
      return `${majorVersion}.${minorVersion + 1}.${revision}`;
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

  isLoading.value = true;

  handleCreateVersion(props.project.projectId, versionType, {
    onSuccess: (version) => emit("create", version),
    onComplete: () => (isLoading.value = false),
  });
}

watch(
  () => props.isOpen,
  (open) => {
    if (!open || !props.project) return;

    getCurrentVersion(props.project.projectId).then(
      (version) => (currentVersion.value = version)
    );
  }
);
</script>
