<template>
  <panel-card>
    <typography el="h2" variant="subtitle" value="Artifact Types" />

    <v-list expand>
      <toggle-list
        v-for="entry in artifactLevels"
        :key="entry.typeId"
        :icon="entry.icon"
        data-cy="list-type-options"
      >
        <template v-slot:activator>
          <typography :value="entry.name" ellipsis />
        </template>
        <v-container>
          <type-direction-input :entry="entry" />
          <type-icon-input :entry="entry" />
        </v-container>
      </toggle-list>
    </v-list>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { TimArtifactLevelSchema } from "@/types";
import { typeOptionsStore } from "@/hooks";
import {
  Typography,
  TypeDirectionInput,
  TypeIconInput,
  ToggleList,
  PanelCard,
} from "@/components/common";

/**
 * Allows a user to edit the artifact type options
 * for a project.
 */
export default Vue.extend({
  name: "TypeOptions",
  components: {
    PanelCard,
    Typography,
    TypeDirectionInput,
    TypeIconInput,
    ToggleList,
  },
  computed: {
    /**
     * @return The current project's artifact types.
     */
    artifactLevels(): TimArtifactLevelSchema[] {
      return typeOptionsStore.artifactLevels;
    },
  },
});
</script>
