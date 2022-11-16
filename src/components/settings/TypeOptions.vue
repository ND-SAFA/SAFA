<template>
  <v-container style="max-width: 50em">
    <panel-card>
      <typography el="h2" variant="subtitle" value="Type Options" />
      <v-divider class="mb-2" />

      <v-list expand class="primary lighten-4">
        <toggle-list
          v-for="entry in typeDirections"
          :key="entry.type"
          :icon="entry.icon"
          data-cy="list-type-options"
        >
          <template v-slot:activator>
            <typography :value="entry.label" ellipsis />
          </template>
          <v-card outlined class="my-2">
            <v-container>
              <type-direction-input :entry="entry" />
              <type-icon-input :entry="entry" />
            </v-container>
          </v-card>
        </toggle-list>
      </v-list>
    </panel-card>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { LabelledTraceDirectionModel } from "@/types";
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
    typeDirections(): LabelledTraceDirectionModel[] {
      return typeOptionsStore.typeDirections();
    },
  },
});
</script>

<style scoped lang="scss"></style>
