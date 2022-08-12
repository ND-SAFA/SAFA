<template>
  <v-container class="mt-2">
    <typography el="h1" variant="title" value="Type Options" />
    <v-divider class="mb-2" />

    <div v-for="entry in artifactDirections" :key="entry.type" class="mt-2">
      <typography el="h2" variant="subtitle" :value="entry.label" />
      <v-divider />

      <typography
        secondary
        el="div"
        y="1"
        :value="`${entry.label} Traces To`"
      />
      <v-chip-group column>
        <v-chip
          v-for="type in entry.allowedTypes"
          :key="type"
          close
          @click:close="handleDeleteDirection(entry, type)"
        >
          <typography :value="getTypeLabel(type)" />
        </v-chip>
      </v-chip-group>
      <v-chip v-if="entry.allowedTypes.length === 0">
        <typography value="Any Type" />
      </v-chip>

      <typography secondary el="div" y="1" :value="`${entry.label} Icon`" />
      <v-btn-toggle v-model="entry.iconIndex" class="my-1" borderless>
        <v-btn
          v-for="option in icons"
          :key="option"
          @change="handleIconChange(entry, option)"
        >
          <v-icon>{{ option }}</v-icon>
        </v-btn>
      </v-btn-toggle>
    </div>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { LabelledTraceDirectionModel } from "@/types";
import { getArtifactTypePrintName } from "@/util";
import { projectModule, typeOptionsModule } from "@/store";
import { handleSaveArtifactType, handleRemoveTraceType } from "@/api";
import { Typography } from "@/components/common";

export default Vue.extend({
  name: "trace-link-direction-tab",
  components: { Typography },
  data() {
    return {
      artifactDirections: [] as LabelledTraceDirectionModel[],
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
    handleIconChange(entry: LabelledTraceDirectionModel, icon: string) {
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
      entry: LabelledTraceDirectionModel,
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
