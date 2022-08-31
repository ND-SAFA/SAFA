<template>
  <div>
    <span class="mt-1">
      <typography bold color="primary" :value="entry.label" />
      <typography secondary value="Icon" />
    </span>
    <v-btn-toggle v-model="entry.iconIndex" class="my-1" borderless>
      <v-btn
        v-for="option in icons"
        :key="option"
        data-cy="button-type-options-icon"
        @change="handleIconChange(entry, option)"
      >
        <v-icon>{{ option }}</v-icon>
      </v-btn>
    </v-btn-toggle>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { LabelledTraceDirectionModel } from "@/types";
import { allTypeIcons } from "@/util";
import { handleSaveArtifactTypeIcon } from "@/api";
import { Typography } from "@/components/common/display";

/**
 * Renders an input for changing the icon for an artifact type.
 */
export default Vue.extend({
  name: "TypeIconInput",
  components: { Typography },
  props: {
    entry: Object as PropType<LabelledTraceDirectionModel>,
  },
  data() {
    return { icons: allTypeIcons };
  },
  methods: {
    /**
     * Updates the icon for an artifact type.
     * @param entry - The type to update.
     * @param icon - The icon to set.
     */
    handleIconChange(entry: LabelledTraceDirectionModel, icon: string) {
      handleSaveArtifactTypeIcon({ ...entry, icon });
    },
  },
});
</script>
