<template>
  <separator />
  <member-symbol />
  <list :items="options">
    <template v-for="item in options" :key="item.title">
      <icon-button
        :fab="false"
        :large="true"
        :tooltip="item.toolTip"
        color="secondary"
        icon-id="mdi-account-circle"
      />
    </template>
  </list>
</template>

<script lang="ts">
export default {
  name: "MembersBar",
};
</script>

<script lang="ts" setup>
import { computed } from "vue";
import { membersStore, sessionStore } from "@/hooks";
import { List, ListItem, IconButton, Separator } from "@/components/common";
import MemberSymbol from "./MemberSymbol.vue";

const members = computed(() => membersStore.activeMembers);

const options = computed(() => {
  return members.value
    .filter((m) => m.email !== sessionStore.userEmail)
    .map((m) => {
      return {
        title: "TITLE",
        iconId: "mdi-math-compass",
        iconTitle: "ICON TITLE",
        toolTip: m.email,
        color: "primary",
      };
    });
});
</script>
