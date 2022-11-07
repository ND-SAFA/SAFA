<template>
  <v-container>
    <typography el="h2" variant="subtitle" value="Type Options" />
    <v-divider class="mb-2" />

    <v-list expand>
      <toggle-list
        v-for="entry in typeDirections"
        :key="entry.type"
        :icon="entry.icon"
        data-cy="list-type-options"
      >
        <template v-slot:activator>
          <v-tooltip bottom open-delay="300">
            <template v-slot:activator="{ on, attrs }">
              <div v-on="on" v-bind="attrs">
                <typography :value="entry.label" ellipsis />
              </div>
            </template>
            <span>
              {{ entry.label }}
            </span>
          </v-tooltip>
        </template>
        <v-card outlined class="my-2">
          <v-container>
            <type-direction-input :entry="entry" />
            <type-icon-input :entry="entry" />
          </v-container>
        </v-card>
      </toggle-list>
    </v-list>
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
} from "@/components/common";

/**
 * Allows a user to edit the artifact type options
 * for a project.
 */
export default Vue.extend({
  name: "TypeOptions",
  components: { Typography, TypeDirectionInput, TypeIconInput, ToggleList },
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
