<template>
  <v-container class="mt-2">
    <typography el="h1" variant="title" value="Type Options" />
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
        <type-direction-input :entry="entry" />
        <type-icon-input :entry="entry" />
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
 * Renders a tab for changing artifact type icons and trace directions.
 */
export default Vue.extend({
  name: "TypeOptionsTab",
  components: { ToggleList, TypeIconInput, TypeDirectionInput, Typography },
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
