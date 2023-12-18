/**
 * Sorts table rows alphabetically.
 * @param rows - The rows to sort.
 * @param sortBy - The item attribute to sort by.
 * @param descending - Whether to sort in descending order.
 */
export function sortRows(
  rows: Record<string, unknown>[],
  sortBy: string | undefined,
  descending: boolean
): Record<string, unknown>[] {
  const sortedRows = [...rows];

  if (sortBy) {
    sortedRows.sort((a, b) => {
      const x = descending ? b : a;
      const y = descending ? a : b;

      return String(x[sortBy]) > String(y[sortBy])
        ? 1
        : String(x[sortBy]) < String(y[sortBy])
          ? -1
          : 0;
    });
  }

  return sortedRows;
}
