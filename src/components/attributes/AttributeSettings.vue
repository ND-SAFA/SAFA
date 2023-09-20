<template>
  <panel-card>
    <q-layout container view="lHh Lpr lff" class="settings-attributes">
      <q-drawer
        v-if="!smallWindow"
        model-value
        persistent
        bordered
        :breakpoint="0"
        :width="260"
      >
        <attribute-editor />
      </q-drawer>
      <q-page-container>
        <q-page class="q-mx-md">
          <attribute-editor v-if="smallWindow" />
          <attribute-layout-editor />
        </q-page>
      </q-page-container>
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
import { useScreen } from "@/hooks";
import { PanelCard } from "@/components/common";
import {
  AttributeEditor,
  AttributeLayoutEditor,
} from "@/components/attributes/save";

const { smallWindow } = useScreen();
</script>
