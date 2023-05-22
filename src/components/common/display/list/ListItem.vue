<template>
  <q-item
    :clickable="itemClickable"
    :v-ripple="!!props.to"
    :to="props.to"
    :color="color"
    :data-cy="dataCy"
    @click="emit('click')"
  >
    <q-tooltip v-if="!!props.tooltip">
      {{ itemTooltip }}
    </q-tooltip>
    <q-item-section v-if="!!props.icon || !!slots.icon" avatar>
      <icon v-if="!!props.icon" :variant="props.icon" />
      <slot name="icon" />
    </q-item-section>
    <q-item-section>
      <q-item-label>
        <typography v-if="!!props.title" :value="props.title" />
        <slot />
        <separator v-if="!!props.divider" t="1" />
      </q-item-label>
      <q-item-label v-if="!!props.subtitle || !!slots.subtitle" caption>
        <typography v-if="!!props.subtitle" secondary :value="props.subtitle" />
        <slot name="subtitle" />
      </q-item-label>
    </q-item-section>
    <q-item-section
      v-if="!!slots.actions"
      :class="props.actionCols ? `col-${props.actionCols}` : ''"
    >
      <div @click.stop="">
        <slot name="actions" />
      </div>
    </q-item-section>
  </q-item>
</template>

<script lang="ts">
/**
 * Displays a generic list item.
 */
export default {
  name: "ListItem",
};
</script>

<script setup lang="ts">
import { computed, useSlots } from "vue";
import { ListItemProps } from "@/types";
import { Typography, Separator } from "../content";
import { Icon } from "../icon";

const props = defineProps<ListItemProps>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const slots = useSlots();

const itemClickable = computed(() => !!(props.clickable || props.to));

const itemTooltip = computed(() => {
  if (typeof props.tooltip === "string") {
    return props.tooltip;
  } else if (props.tooltip === true) {
    return props.subtitle ? `${props.title} - ${props.subtitle}` : props.title;
  } else {
    return undefined;
  }
});
</script>
