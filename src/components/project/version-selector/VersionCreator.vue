<template>
  <generic-modal
    :title="`Current Version: ${versionToString(currentVersion)}`"
    size="xs"
    :is-open="isOpen"
    :actions-height="0"
    v-bind:isLoading.sync="isLoading"
    @close="onClose"
  >
    <template v-slot:body>
      <v-container class="mt-2">
        <v-row justify="center">
          <v-btn
            outlined
            text
            block
            color="primary"
            @click="() => onClick('major')"
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
            @click="() => onClick('minor')"
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
            @click="() => onClick('revision')"
          >
            New Revision: {{ nextVersion("revision") }}</v-btn
          >
        </v-row>
      </v-container>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectIdentifier, ProjectVersion, VersionType } from "@/types";
import { versionToString } from "@/util";
import {
  createMajorVersion,
  createMinorVersion,
  createRevisionVersion,
  getCurrentVersion,
} from "@/api";
import { GenericModal } from "@/components/common";

/**
 * A modal for creating new versions.
 *
 * @emits-1 `create` (ProjectVersion) - On version creation.
 * @emits-2 `close` - On close.
 */
export default Vue.extend({
  components: {
    GenericModal,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
  },
  data() {
    return {
      isLoading: false,
      currentVersion: undefined as ProjectVersion | undefined,
    };
  },
  methods: {
    versionToString(): string {
      return versionToString(this.currentVersion);
    },
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
    onClick(versionType: VersionType) {
      const projectId = this.project?.projectId;

      if (projectId === undefined) {
        throw Error("project expected to be defined");
      }

      const createVersionFrom = async (
        createVersion: (projectId: string) => Promise<ProjectVersion>
      ) => {
        this.isLoading = true;

        const version = await createVersion(projectId);

        this.$emit("create", version);
        this.isLoading = false;
      };

      switch (versionType) {
        case "major":
          createVersionFrom(createMajorVersion);
          break;
        case "minor":
          createVersionFrom(createMinorVersion);
          break;
        case "revision":
          createVersionFrom(createRevisionVersion);
          break;
        default:
          throw Error("Unknown type" + versionType);
      }
    },
    onClose() {
      this.$emit("close");
    },
  },

  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen && this.project) {
        getCurrentVersion(this.project.projectId).then(
          (version) => (this.currentVersion = version)
        );
      }
    },
  },
});
</script>
