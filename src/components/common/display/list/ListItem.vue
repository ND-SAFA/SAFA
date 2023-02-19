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
        <q-separator v-if="!!props.divider" class="q-mt-sm" />
      </q-item-label>
      <q-item-label v-if="!!props.subtitle || !!slots.subtitle" caption>
        <typography v-if="!!props.subtitle" secondary :value="props.subtitle" />
        <slot name="subtitle" />
      </q-item-label>
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
import { IconVariant, URLQuery } from "@/types";
import Typography from "../Typography.vue";
import { Icon } from "../icon";

const props = defineProps<{
  title?: string;
  subtitle?: string;
  tooltip?: true | string;
  icon?: IconVariant;
  clickable?: boolean;
  to?: string | { path: string; query: URLQuery };
  color?: string;
  divider?: boolean;
  dataCy?: string;
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

const emit = defineEmits<{
  (e: "click"): void;
}>();
</script>
