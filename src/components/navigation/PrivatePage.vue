<template>
  <q-page v-if="doDisplay" :padding="!props.fullWindow">
    <div class="q-mx-auto" :style="style">
      <flex-box v-if="!!props.title" justify="between" align="center">
        <typography el="h1" variant="title" value="My Account" />
        <slot name="actions" />
      </flex-box>
      <separator v-if="!!props.title" b="4" />
      <typography
        v-if="!!props.subtitle"
        el="p"
        y="2"
        value="Create a project using one of the following methods."
      />
      <slot />
    </div>
  </q-page>
  <q-page v-else>
    <div class="full-width" style="margin-top: 40vh">
      <div class="q-mx-auto width-fit">
        <q-circular-progress
          rounded
          indeterminate
          size="60px"
          :thickness="0.2"
          color="primary"
        />
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
/**
 * Displays a page with top and sidebars.
 */
export default {
  name: "PrivatePage",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { sessionStore } from "@/hooks";
import { FlexBox, Typography, Separator } from "@/components/common";

const props = defineProps<{
  fullWindow?: boolean;
  title?: string;
  subtitle?: string;
}>();

const doDisplay = computed(() => sessionStore.doesSessionExist);
const style = computed(() => (props.fullWindow ? "" : "max-width: 1000px"));
</script>
