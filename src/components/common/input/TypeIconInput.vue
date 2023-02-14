<template>
  <div>
    <div class="mt-1">
      <typography bold color="primary" :value="entry.name" />
      <typography secondary value="Icon:" />
    </div>
    <v-btn-toggle v-model="entry.iconIndex" class="my-1" borderless>
      <v-btn
        v-for="option in icons"
        :key="option"
        :disabled="!allowEditing"
        data-cy="button-type-options-icon"
        @change="handleIconChange(entry, option)"
      >
        <v-icon>{{ option }}</v-icon>
      </v-btn>
    </v-btn-toggle>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { TimArtifactLevelSchema } from "@/types";
import { allTypeIcons } from "@/util";
import { projectStore, sessionStore } from "@/hooks";
import { handleSaveArtifactTypeIcon } from "@/api";
import { Typography } from "@/components/common/display";

/**
 * Renders an input for changing the icon for an artifact type.
 */
export default defineComponent({
  name: "TypeIconInput",
  components: { Typography },
  props: {
    entry: Object as PropType<TimArtifactLevelSchema>,
  },
  data() {
    return { icons: allTypeIcons };
  },
  computed: {
    /**
     * @return Whether to allow editing.
     */
    allowEditing(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
  },
  methods: {
    /**
     * Updates the icon for an artifact type.
     * @param entry - The type to update.
     * @param icon - The icon to set.
     */
    handleIconChange(entry: TimArtifactLevelSchema, icon: string) {
      handleSaveArtifactTypeIcon({ ...entry, icon });
    },
  },
});
</script>
