<template>
  <typography variant="subtitle" el="h3" value="Team members" />
  <separator />
  <member-table minimal :entity="entity" />
</template>

<script lang="ts">
/**
 * A table for managing members of a team.
 */
export default {
  name: "TeamMemberTable",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { MemberEntitySchema } from "@/types";
import { projectStore } from "@/hooks";
import Separator from "@/components/common/display/content/Separator.vue";
import { Typography } from "@/components";
import MemberTable from "./MemberTable.vue";

const entity = computed(
  () =>
    ({
      entityType: "TEAM",
      entityId: projectStore.projectId,
    } as MemberEntitySchema)
);
</script>
