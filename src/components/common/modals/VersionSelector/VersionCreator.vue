<template>
  <GenericModal
    title="Create new version"
    :isOpen="isOpen"
    :size="m"
    @onClose="onClose"
  >
    <template v-slot:body>
      <v-container>
        <v-row justify="center">
          CurrentVersion: {{ versionToString(currentVersion) }}
        </v-row>
        <v-row justify="center" class="mt-5">
          <v-btn outlined text color="primary" @click="() => onClick('major')">
            New Major Version: {{ nextVersion("major") }}
          </v-btn>
        </v-row>
        <v-row justify="center" class="mt-5">
          <v-btn outlined text color="primary" @click="() => onClick('minor')">
            New Minor Version: {{ nextVersion("minor") }}
          </v-btn>
        </v-row>
        <v-row justify="center" class="mt-5">
          <v-btn
            outlined
            text
            color="primary"
            @click="() => onClick('revision')"
          >
            New Revision: {{ nextVersion("revision") }}</v-btn
          >
        </v-row>
      </v-container>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import {
  createNewMajorVersion,
  createNewMinorVersion,
  createNewRevisionVersion,
  getCurrentVersion,
} from "@/api/project-api";
import { ProjectIdentifier, ProjectVersion } from "@/types/domain/project";
import Vue, { PropType } from "vue";
import { versionToString } from "@/util/to-string";
import GenericModal from "@/components/common/modals/GenericModal.vue";

type VersionType = "major" | "minor" | "revision";

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
      if (this.project === undefined) {
        throw Error("project expected to be defined");
      }
      const projectId = this.project.projectId;
      let creationPromise: Promise<ProjectVersion>;
      switch (versionType) {
        case "major":
          creationPromise = createNewMajorVersion(projectId);
          break;
        case "minor":
          creationPromise = createNewMinorVersion(projectId);
          break;
        case "revision":
          creationPromise = createNewRevisionVersion(projectId);
          break;
        default:
          throw Error("Unknown type" + versionType);
      }
      creationPromise.then((version: ProjectVersion) => {
        this.$emit("onCreate", version);
      });
    },
    onClose() {
      this.$emit("onClose");
    },
  },

  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen) {
        getCurrentVersion(this.project.projectId).then(
          (version) => (this.currentVersion = version)
        );
      }
    },
  },
});
</script>
