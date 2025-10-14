<template>
  <member-table :entity="entity" />
</template>

<script lang="ts">
/**
 * A table for managing members of a project.
 */
export default {
  name: "ProjectMemberTable",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { MemberEntitySchema } from "@/types";
import { projectStore } from "@/hooks";
import MemberTable from "./MemberTable.vue";

const entity = computed(
  () =>
    ({
      entityType: "PROJECT",
      entityId: projectStore.projectId,
    }) as MemberEntitySchema
);
</script>
