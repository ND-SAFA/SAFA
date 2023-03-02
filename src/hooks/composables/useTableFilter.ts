import { computed, ref } from "vue";
import { TableFilterHook, TableFilterProps } from "@/types";

/**
 * A hook for filtering table rows.
 *
 * @param props - The filter props to filter table rows with.
 * @return A hook with the filtered rows.
 */
export function useTableFilter(props: TableFilterProps): TableFilterHook {
  const searchText = ref<string | null>("");

  const searchLabel = computed(() =>
    props.itemName ? `Search ${props.itemName}s` : "Search"
  );

  const lowercaseSearchText = computed(() =>
    (searchText.value || "").toLowerCase()
  );

  const columnKeys = computed(() => props.columns.map(({ name }) => name));

  const filteredRows = computed(() =>
    props.rows.filter((row) => {
      for (const key of columnKeys.value) {
        if (
          String(row[key]).toLowerCase().includes(lowercaseSearchText.value)
        ) {
          return true;
        }
      }

      return false;
    })
  );

  return { searchText, searchLabel, filteredRows };
}
