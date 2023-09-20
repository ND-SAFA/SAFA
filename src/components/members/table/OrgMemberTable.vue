<template>
  <member-table :entity="entity" />
</template>

<script lang="ts">
/**
 * A table for managing members of an organization.
 */
export default {
  name: "OrgMemberTable",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { MemberEntitySchema } from "@/types";
import { orgStore } from "@/hooks";
import MemberTable from "./MemberTable.vue";

const entity = computed(
  () =>
    ({
      entityType: "ORGANIZATION",
      entityId: orgStore.orgId,
    }) as MemberEntitySchema
);
</script>
