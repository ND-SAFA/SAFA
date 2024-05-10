<template>
  <q-item
    :clickable="itemClickable"
    :v-ripple="!!props.to"
    :to="props.to"
    :data-cy="dataCy"
    :dense="smallWindow"
    @click="emit('click')"
  >
    <q-tooltip v-if="!!props.tooltip">
      {{ itemTooltip }}
    </q-tooltip>
    <q-item-section
      v-if="!!props.icon || !!props.iconId || !!slots.icon"
      avatar
    >
      <flex-box column align="center" justify="center">
        <icon
          v-if="!!props.icon || !!props.iconId"
          :id="props.iconId"
          :variant="props.icon"
          :color="props.color"
          size="sm"
        />
        <slot name="icon" />
        <typography
          v-if="!!props.iconTitle"
          :value="props.iconTitle"
          variant="small"
          align="center"
          :color="props.color"
        />
      </flex-box>
    </q-item-section>
    <q-item-section>
      <q-item-label class="text-ellipsis">
        <typography v-if="!!props.title" :value="props.title" ellipsis />
        <slot />
        <separator v-if="props.divider" t="1" />
      </q-item-label>
      <q-item-label
        v-if="!!props.subtitle || !!slots.subtitle"
        caption
        class="text-ellipsis"
      >
        <typography
          v-if="!!props.subtitle"
          secondary
          :value="props.subtitle"
          ellipsis
        />
        <slot name="subtitle" />
      </q-item-label>
    </q-item-section>
    <q-item-section
      v-if="!!slots.actions"
      :class="props.actionCols ? `col-${props.actionCols}` : 'width-fit'"
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
import { useScreen } from "@/hooks";
import FlexBox from "@/components/common/display/content/FlexBox.vue";
import { Typography, Separator } from "../content";
import { Icon } from "../icon";

const props = defineProps<ListItemProps>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const slots = useSlots();
const { smallWindow } = useScreen();

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
