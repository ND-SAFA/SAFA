<template>
  <q-page v-if="doDisplay" :padding="!props.fullWindow">
    <div v-if="!props.graph" :class="className">
      <back-button v-if="props.backToProject" to-project class="q-mb-sm" />
      <flex-box v-if="!!props.title" justify="between" align="center">
        <typography el="h1" variant="title" :value="props.title" />
        <slot name="actions" />
      </flex-box>
      <separator v-if="!!props.title" b="2" />
      <typography
        v-if="!!props.subtitle"
        el="p"
        b="2"
        :value="props.subtitle"
      />
      <slot />
    </div>
    <slot v-else />
  </q-page>
  <q-page v-else>
    <div class="full-width nav-page-loading">
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
import { PrivatePageProps } from "@/types";
import { sessionStore } from "@/hooks";
import {
  FlexBox,
  Typography,
  Separator,
  BackButton,
} from "@/components/common";

const props = defineProps<PrivatePageProps>();

const doDisplay = computed(() => sessionStore.doesSessionExist);

const className = computed(() =>
  props.fullWindow
    ? "q-mx-auto q-pa-xl"
    : "q-mx-auto q-pa-lg nav-page-centered " +
      (props.smallWindow ? "width-fit" : "")
);
</script>
