<template>
  <panel-card
    :title="title"
    subtitle="View recent transactions for this organization."
  >
    <groupable-table
      :columns="transactionsColumns"
      :rows="transactions"
      row-key="id"
      item-name="Transaction"
      default-sort-desc
      default-sort-by="timestamp"
    >
      <template #header-right>
        <select-input
          v-model="mode"
          outlined
          dense
          label="Period"
          class="q-mb-sm"
          :options="modeOptions"
        />
      </template>
    </groupable-table>
  </panel-card>
</template>

<script lang="ts">
/**
 * A tab for managing teams within an organization.
 */
export default {
  name: "TransactionTab",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { transactionsColumns } from "@/util";
import { orgStore } from "@/hooks";
import { PanelCard, SelectInput, GroupableTable } from "@/components/common";

const modeOptions = ["All", "Monthly"];

const mode = ref<"All" | "Monthly">("Monthly");

const title = computed(() =>
  mode.value === "All" ? "All Transactions" : "Monthly Transactions"
);

const transactions = computed(() =>
  mode.value == "All" ? orgStore.allTransactions : orgStore.monthlyTransactions
);
</script>
