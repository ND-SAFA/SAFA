<template>
  <v-container>
    <h1 class="text-h4 my-2">Type Options</h1>
    <div v-for="entry in artifactDirections" :key="entry.type">
      <h2 class="text-h5 mb-2">{{ entry.label }}</h2>

      <h3 class="text-h6">{{ entry.label }} Can Trace To</h3>

      <v-chip-group column>
        <v-chip
          v-for="type in entry.allowedTypes"
          :key="type"
          close
          @click:close="onDeleteDirection(entry, type)"
        >
          {{ getTypeLabel(type) }}
        </v-chip>
      </v-chip-group>

      <v-chip v-if="entry.allowedTypes.length === 0">
        Any Type of Artifact
      </v-chip>

      <h3 class="text-h6 mb-1">{{ entry.label }} Icon</h3>

      <v-btn-toggle v-model="entry.iconIndex">
        <v-btn
          v-for="option in icons"
          :key="option"
          @change="onIconChange(entry, option)"
        >
          <v-icon>{{ option }}</v-icon>
        </v-btn>
      </v-btn-toggle>

      <v-divider class="my-4" />
    </div>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { LabeledArtifactDirection } from "@/types";
import { getArtifactTypePrintName } from "@/util";
import { logModule, projectModule, typeOptionsModule } from "@/store";
import { handleSaveArtifactType, handleRemoveTraceType } from "@/api";

export default Vue.extend({
  name: "trace-link-direction-tab",
  data() {
    return {
      artifactTypes: [] as string[],
      artifactDirections: [] as LabeledArtifactDirection[],
    };
  },
  mounted() {
    this.artifactTypes = typeOptionsModule.artifactTypes;

    this.artifactDirections = Object.entries(
      typeOptionsModule.linkDirections
    ).map(([type, allowedTypes]) => {
      const icon = typeOptionsModule.getArtifactTypeIcon(type);

      return {
        type,
        allowedTypes,
        label: this.getTypeLabel(type),
        icon,
        iconIndex: this.icons.indexOf(icon),
      };
    });
  },
  computed: {
    icons(): string[] {
      return typeOptionsModule.allArtifactTypeIcons;
    },
  },
  methods: {
    getTypeLabel(type: string) {
      return getArtifactTypePrintName(type);
    },
    onIconChange(entry: LabeledArtifactDirection, icon: string) {
      const artifactTypeQuery = projectModule.getProject.artifactTypes.filter(
        (a) => a.name === entry.type
      );

      if (artifactTypeQuery.length === 1) {
        typeOptionsModule.updateArtifactIcon({ ...entry, icon });
        handleSaveArtifactType({ ...artifactTypeQuery[0], icon });
      } else {
        logModule.onWarning("Unable to find artifact type: " + entry.label);
      }
    },
    onDeleteDirection(entry: LabeledArtifactDirection, removedType: string) {
      entry.allowedTypes = entry.allowedTypes.filter(
        (allowedType) => allowedType !== removedType
      );

      typeOptionsModule.updateLinkDirections(entry);
      handleRemoveTraceType(entry.type, removedType);
    },
  },
});
</script>

<style>
.v-autocomplete.v-select--is-menu-active .v-input__icon--append .v-icon {
  transform: none !important;
}
</style>
