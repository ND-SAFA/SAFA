<template>
  <panel-card>
    <q-layout container view="lHh Lpr lff" style="min-height: 60vh">
      <q-drawer
        v-if="!smallWindow"
        model-value
        persistent
        bordered
        :breakpoint="0"
        :width="280"
      >
        <attribute-editor />
      </q-drawer>
      <attribute-editor v-else />
      <attribute-layout-editor />
    </q-layout>
  </panel-card>
</template>

<script lang="ts">
/**
 * Renders settings for customizing artifact attributes.
 */
export default {
  name: "AttributeSettings",
};
</script>

<script setup lang="ts">
import { useQuasar } from "quasar";
import { computed } from "vue";
import { PanelCard } from "@/components/common";
import AttributeEditor from "./AttributeEditor.vue";
import AttributeLayoutEditor from "./AttributeLayoutEditor.vue";

const $q = useQuasar();

const smallWindow = computed(() => $q.screen.lt.lg);
</script>
