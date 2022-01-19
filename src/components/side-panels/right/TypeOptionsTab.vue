<template>
  <v-container>
    <h1 class="text-h4 my-2">Type Options</h1>
    <div v-for="entry in artifactDirections" :key="entry.type">
      <h2 class="text-h5 mb-2">{{ entry.label }}</h2>
      <v-autocomplete
        filled
        multiple
        chips
        deletable-chips
        small-chips
        hide-details
        v-model="entry.allowedTypes"
        :items="artifactTypes"
        :label="entry.label + ' Trace To'"
        @change="onDirectionChange(entry)"
      />

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
import { typeOptionsModule } from "@/store";

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
        label: getArtifactTypePrintName(type),
        icon: typeOptionsModule.getArtifactTypeIcon(type),
        iconIndex: this.icons.indexOf(icon),
      };
    });
  },
  computed: {
    icons(): string[] {
      return Object.values(typeOptionsModule.allArtifactTypeIcons);
    },
  },
  methods: {
    onDirectionChange(entry: LabeledArtifactDirection) {
      typeOptionsModule.updateLinkDirections(entry);
    },
    onIconChange(entry: LabeledArtifactDirection, icon: string) {
      typeOptionsModule.updateArtifactIcon({ ...entry, icon });
    },
  },
});
</script>

<style>
.v-autocomplete.v-select--is-menu-active .v-input__icon--append .v-icon {
  transform: none !important;
}
</style>
