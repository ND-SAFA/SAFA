<template>
  <list-item
    :clickable="clickable"
    :color="color"
    :title="props.title"
    :subtitle="props.hasCredentials ? 'Connected' : 'Not Connected'"
    @click="emit('click')"
  >
    <template #icon>
      <icon v-if="!props.loading" :color="color" variant="integrate" />
      <q-circular-progress v-else indeterminate />
    </template>
    <template #actions>
      <text-button
        v-if="!props.hasCredentials"
        label="Connect"
        color="primary"
        outlined
        icon="integrate"
        @click="emit('connect')"
      />
      <flex-box v-else column align="end">
        <text-button
          outlined
          label="Installation"
          icon="add"
          b="2"
          @click="emit('connect')"
        />
        <text-button
          outlined
          label="Disconnect"
          icon="delete"
          @click="emit('disconnect')"
        />
      </flex-box>
    </template>
  </list-item>
</template>

<script lang="ts">
/**
 * Displays a list item & buttons for authenticating an integration.
 */
export default {
  name: "AuthenticationListItem",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { TextButton, FlexBox, Icon } from "@/components/common";
import ListItem from "@/components/common/display/list/ListItem.vue";

const props = defineProps<{
  hasCredentials: boolean;
  loading?: boolean;
  title: string;
  inactive?: boolean;
}>();

const emit = defineEmits<{
  (e: "click"): void;
  (e: "connect"): void;
  (e: "disconnect"): void;
}>();

const color = computed(() => (props.hasCredentials ? "positive" : "grey"));
const clickable = computed(() => !props.inactive && props.hasCredentials);
</script>
