import { computed, ref } from "vue";
import { TableFilterHook, TableFilterProps } from "@/types";
import { sortRows } from "@/util";

/**
 * A hook for sorting and filtering table rows.
 *
 * @param props - The filter props to filter table rows with.
 * @return A hook with the filtered rows.
 */
export function useTableFilter(props: TableFilterProps): TableFilterHook {
  const searchText = ref<string | null>("");
  const sortBy = ref<string | undefined>(props.defaultSortBy);
  const sortDesc = ref(props.defaultSortDesc || false);

  const searchLabel = computed(() =>
    props.itemName ? `Search ${props.itemName}s` : "Search"
  );

  const lowercaseSearchText = computed(() =>
    (searchText.value || "").toLowerCase()
  );

  const sortedRows = computed(() =>
    sortRows(props.rows, sortBy.value, sortDesc.value)
  );

  const columnKeys = computed(() => props.columns.map(({ name }) => name));

  const filteredRows = computed(() =>
    sortedRows.value.filter((row) => {
      if (props.filterRow && !props.filterRow(row)) {
        return false;
      }

      for (const key of [...columnKeys.value, "body", "summary"]) {
        if (
          row[key] !== undefined &&
          String(row[key]).toLowerCase().includes(lowercaseSearchText.value)
        ) {
          return true;
        }
      }

      return false;
    })
  );

  return {
    searchText,
    searchLabel,
    sortBy,
    sortDesc,
    filteredRows,
  };
}
