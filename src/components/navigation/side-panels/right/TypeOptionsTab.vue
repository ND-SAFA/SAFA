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
          @click:close="handleDeleteDirection(entry, type)"
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
          @change="handleIconChange(entry, option)"
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
import { projectModule, typeOptionsModule } from "@/store";
import { handleSaveArtifactType, handleRemoveTraceType } from "@/api";

export default Vue.extend({
  name: "trace-link-direction-tab",
  data() {
    return {
      artifactDirections: [] as LabeledArtifactDirection[],
      icons: typeOptionsModule.allArtifactTypeIcons,
    };
  },
  /**
   * Update artifact type directions on mount.
   */
  mounted() {
    this.generateTypeDirections();
  },
  computed: {
    /**
     * @return The current project's artifact types.
     */
    artifactTypes(): string[] {
      return typeOptionsModule.artifactTypes;
    },
  },
  methods: {
    /**
     * Converts an artifact type to a title case name.
     * @param type - The type to convert.
     * @return The type display name.
     */
    getTypeLabel(type: string) {
      return getArtifactTypePrintName(type);
    },
    /**
     * Updates the icon for an artifact type.
     * @param entry - The type to update.
     * @param icon - The icon to set.
     */
    handleIconChange(entry: LabeledArtifactDirection, icon: string) {
      const type = projectModule.getProject.artifactTypes.find(
        ({ name }) => name === entry.type
      );

      if (!type) return;

      typeOptionsModule.updateArtifactIcon({ ...entry, icon });
      handleSaveArtifactType({ ...type, icon });
    },
    /**
     * Removes an artifact type direction.
     * @param entry - The type to update.
     * @param removedType - The type to remove.
     */
    handleDeleteDirection(
      entry: LabeledArtifactDirection,
      removedType: string
    ) {
      entry.allowedTypes = entry.allowedTypes.filter(
        (allowedType) => allowedType !== removedType
      );

      typeOptionsModule.updateLinkDirections(entry);
      handleRemoveTraceType(entry.type, removedType);
    },
    /**
     * Generates artifact type directions for the current artifact types.
     */
    generateTypeDirections() {
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
  },
  watch: {
    /**
     * Update artifact type directions when the types change.
     */
    artifactTypes() {
      this.generateTypeDirections();
    },
  },
});
</script>

<style>
.v-autocomplete.v-select--is-menu-active .v-input__icon--append .v-icon {
  transform: none !important;
}
</style>
