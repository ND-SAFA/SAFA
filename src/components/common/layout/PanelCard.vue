<template>
  <div :class="containerClassName">
    <q-card flat :class="className">
      <flex-box v-if="!props.minimal" align="center" justify="between">
        <flex-box align="center">
          <icon
            v-if="!!props.icon"
            :variant="props.icon"
            class="q-mr-sm"
            size="lg"
          />
          <typography
            v-if="!!props.title"
            variant="subtitle"
            el="h2"
            :value="props.title"
            ellipsis
          />
        </flex-box>
        <slot name="title-actions" />
      </flex-box>
      <separator v-if="!props.minimal && !!props.title" b="2" />
      <typography
        v-if="!props.minimal && !!props.subtitle"
        el="p"
        b="4"
        :value="props.subtitle"
      />
      <slot />
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
import { computed, useSlots, withDefaults } from "vue";
import { PanelCardProps } from "@/types";
import {
  Typography,
  Icon,
  Separator,
  FlexBox,
} from "@/components/common/display";

const props = withDefaults(defineProps<PanelCardProps>(), {
  color: "primary",
  title: undefined,
  subtitle: undefined,
  icon: undefined,
  class: "",
  containerClass: "",
});

const slots = useSlots();

const color = computed(() => (props.minimal ? "transparent" : props.color));

const padding = computed(() => (props.minimal ? "q-pa-xs" : "q-pa-md"));

const className = computed(
  () =>
    `overflow-hidden bg-neutral ${padding.value} bd-${color.value} ${props.class}`
);

const containerClassName = computed(() => `q-mb-md ${props.containerClass}`);
</script>
