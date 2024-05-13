<template>
  <div :class="containerClassName">
    <q-card flat :class="className">
      <flex-box v-if="!props.minimal" align="center" justify="between">
        <flex-box align="center" class="overflow-hidden">
          <icon
            v-if="!!props.icon"
            :variant="props.icon"
            class="q-mr-sm"
            size="lg"
            color="primary"
          />
          <typography
            v-if="!!props.title"
            variant="subtitle"
            el="h2"
            :value="props.title"
            ellipsis
          />
          <slot name="title" />
        </flex-box>

        <flex-box
          v-if="props.collapsable || !!slots['title-actions']"
          align="center"
        >
          <slot v-if="!props.collapsable || expanded" name="title-actions" />
          <icon-button
            v-if="props.collapsable"
            small
            tooltip="Toggle expanded"
            :icon="expanded ? 'up' : 'down'"
            @click="expanded = !expanded"
          />
        </flex-box>
      </flex-box>

      <separator
        v-if="!props.minimal && (!!props.title || !!slots.title) && expanded"
        b="2"
      />

      <typography
        v-if="!props.minimal && !!props.subtitle && expanded"
        el="p"
        b="4"
        :value="props.subtitle"
        secondary
      />

      <slot v-if="expanded" />

      <q-card-actions v-if="!!slots.actions">
        <slot name="actions" />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script lang="ts">
/**
 * Displays a card that contains panel content.
 */
export default {
  name: "PanelCard",
};
</script>

<script setup lang="ts">
import { computed, ref, useSlots, withDefaults } from "vue";
import { PanelCardProps } from "@/types";
import {
  Typography,
  Icon,
  Separator,
  FlexBox,
} from "@/components/common/display";
import IconButton from "@/components/common/button/IconButton.vue";

const props = withDefaults(defineProps<PanelCardProps>(), {
  color: "border",
  title: undefined,
  subtitle: undefined,
  icon: undefined,
  class: "",
  containerClass: "",
  borderless: false,
});

const slots = useSlots();

const expanded = ref(true);

const color = computed(() => (props.minimal ? "transparent" : props.color));

const padding = computed(() => {
  if (props.borderless) {
    return "q-px-md";
  } else if (props.minimal) {
    return "q-pa-xs";
  } else {
    return "q-pa-md";
  }
});

const className = computed(
  () =>
    `overflow-hidden bg-neutral ${padding.value} ` +
    (props.borderless ? " " : `bd-${color.value} `) +
    props.class
);

const containerClassName = computed(() => `q-mb-md ${props.containerClass}`);
</script>
