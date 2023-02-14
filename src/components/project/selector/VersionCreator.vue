<template>
  <modal
    v-model:is-loading="isLoading"
    :title="`Current Version: ${version}`"
    size="xs"
    :is-open="isOpen"
    :actions-height="0"
    data-cy="modal-version-create"
    @close="handleClose"
  >
    <template #body>
      <v-container class="mt-2">
        <v-row justify="center">
          <v-btn
            outlined
            text
            block
            color="primary"
            data-cy="button-create-major-version"
            @click="() => handleClick('major')"
          >
            New Major Version: {{ nextVersion("major") }}
          </v-btn>
        </v-row>
        <v-row justify="center" class="mt-5">
          <v-btn
            outlined
            text
            block
            color="primary"
            data-cy="button-create-minor-version"
            @click="() => handleClick('minor')"
          >
            New Minor Version: {{ nextVersion("minor") }}
          </v-btn>
        </v-row>
        <v-row justify="center" class="mt-5">
          <v-btn
            outlined
            text
            block
            color="primary"
            data-cy="button-create-revision-version"
            @click="() => handleClick('revision')"
          >
            New Revision: {{ nextVersion("revision") }}
          </v-btn>
        </v-row>
      </v-container>
    </template>
  </modal>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { IdentifierSchema, VersionSchema, VersionType } from "@/types";
import { versionToString } from "@/util";
import { getCurrentVersion, handleCreateVersion } from "@/api";
import { Modal } from "@/components/common";

/**
 * A modal for creating new versions.
 *
 * @emits-1 `create` (ProjectVersion) - On version creation.
 * @emits-2 `close` - On close.
 */
export default defineComponent({
  name: "VersionCreator",
  components: {
    Modal,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<IdentifierSchema>,
      required: false,
    },
  },
  data() {
    return {
      isLoading: false,
      currentVersion: undefined as VersionSchema | undefined,
    };
  },
  computed: {
    /**
     * @return The version name.
     */
    version(): string {
      return versionToString(this.currentVersion);
    },
  },
  watch: {
    /**
     * Gets the current version when opened.
     */
    isOpen(open: boolean) {
      if (!open || !this.project) return;

      getCurrentVersion(this.project.projectId).then(
        (version) => (this.currentVersion = version)
      );
    },
  },
  methods: {
    /**
     * Returns the next version name.
     * @param type - The type of new version.
     */
    nextVersion(type: VersionType): string {
      if (this.currentVersion === undefined) {
        return "X.X.X";
      }
      const { majorVersion, minorVersion, revision } = this.currentVersion;
      switch (type) {
        case "major":
          return `${majorVersion + 1}.${minorVersion}.${revision}`;
        case "minor":
          return `${majorVersion}.${minorVersion + 1}.${revision}`;
        case "revision":
          return `${majorVersion}.${minorVersion}.${revision + 1}`;
        default:
          return "X.X.X";
      }
    },
    /**
     * Creates a new version.
     * @param versionType - The version type to create.
     */
    handleClick(versionType: VersionType) {
      if (!this.project) return;

      this.isLoading = true;

      handleCreateVersion(this.project.projectId, versionType, {
        onSuccess: (version) => this.$emit("create", version),
        onComplete: () => (this.isLoading = false),
      });
    },
    /**
     * Emits a request to close the modal.
     */
    handleClose() {
      this.$emit("close");
    },
  },
});
</script>
