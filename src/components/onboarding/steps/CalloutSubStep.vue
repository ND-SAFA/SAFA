<template>
  <q-banner rounded :class="className">
    <template #avatar>
      <icon :variant="iconVariant" :color="color" size="md" />
    </template>
    <typography :value="props.message" />
    <template #action>
      <slot name="action" />
      <text-button
        v-if="!slots.action"
        text
        :color="color"
        icon="calendar"
        @click="onboardingStore.handleScheduleCall(props.status === 'error')"
      >
        Schedule a Call
      </text-button>
    </template>
  </q-banner>
</template>

<script lang="ts">
/**
 * A substep in the onboarding process that displays a callout message.
 */
export default {
  name: "CalloutSubStep",
};
</script>

<script setup lang="ts">
import { computed, useSlots } from "vue";
import { IconVariant } from "@/types";
import { onboardingStore } from "@/hooks";
import { Icon, TextButton, Typography } from "@/components";

const props = defineProps<{
  icon?: IconVariant;
  message: string;
  status?: "error" | "success";
}>();

const slots = useSlots();

const iconVariant = computed(() => {
  if (props.icon) {
    return props.icon;
  } else if (props.status === "error") {
    return "error";
  } else if (props.status === "success") {
    return "success";
  } else {
    return "info";
  }
});

const color = computed(() => {
  if (props.status === "error") {
    return "negative";
  } else if (props.status === "success") {
    return "primary";
  } else {
    return "secondary";
  }
});

const className = computed(() => `bd-${color.value} q-mt-md`);
</script>
