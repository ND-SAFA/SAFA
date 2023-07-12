<template>
  <q-card
    :bordered="visible"
    flat
    :class="visible ? 'bd-primary q-mx-sm' : 'q-mx-sm'"
  >
    <q-btn-group flat>
      <icon-button
        v-for="level of artifactLevels"
        v-show="visible"
        :key="level.id"
        v-bind="buttonProps(level)"
        dense
        :tooltip-delay="0"
        icon="artifact"
        data-cy="button-filter-type"
        @click="emit('click', level, artifactLevels)"
      />
      <separator v-show="visible" vertical color="primary" />
      <icon-button
        dense
        tooltip="Filter Types"
        color="primary"
        :icon="visible ? 'filter-close' : 'filter-open'"
        @click="visible = !visible"
      />
    </q-btn-group>
  </q-card>
</template>

<script lang="ts">
/**
 * Buttons for selecting artifact types.
 */
export default {
  name: "TypeButtons",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { TimArtifactLevelSchema } from "@/types";
import { typeOptionsStore } from "@/hooks";
import { IconButton, Separator } from "@/components/common";

const props = defineProps<{
  /**
   * Whether the buttons are visible by default.
   * @default false
   */
  defaultVisible?: boolean;
  /**
   * Which type buttons are not active.
   * Defaults to all buttons being active.
   */
  hiddenTypes: string[];
}>();

const emit = defineEmits<{
  /**
   * Emitted when a type option is selected.
   */
  (
    e: "click",
    option: TimArtifactLevelSchema,
    allOptions: TimArtifactLevelSchema[]
  ): void;
}>();

const visible = ref(props.defaultVisible || false);

const artifactLevels = computed(() => typeOptionsStore.artifactLevels);

/**
 * Returns props for a type button.
 * @param option - The type button to get props for.
 */
function buttonProps(option: TimArtifactLevelSchema) {
  const hidden = props.hiddenTypes.find((type) => type === option.name);

  return {
    style: `color: ${option.color};` + (hidden ? "opacity: 0.3" : ""),
    tooltip: option.name,
    class: !hidden ? "nav-mode-selected" : "",
  };
}
</script>
