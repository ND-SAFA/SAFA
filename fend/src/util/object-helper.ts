/**
 * Converts a value or an object containing that value to the value itself.
 *
 * @param objOrValue - A value, or an object containing the same value.
 * @param key - The key of the object containing the value.
 * @return The standardized value.
 */
export function standardizeValue<
  T extends string,
  V extends string | number | boolean,
>(objOrValue: V | Record<T, V>, key: T): V {
  return typeof objOrValue === "object" ? objOrValue[key] : objOrValue;
}

/**
 * Converts a list of values, or objects containing those values, to a list of the value itself.
 *
 * @param objOrValueArray - A list of values, or objects containing those values.
 * @param key - The key of the object containing the value.
 * @return The standardized value array.
 */
export function standardizeValueArray<T extends string>(
  objOrValueArray: string[] | Record<T, string>[],
  key: T
): string[] {
  return objOrValueArray.map((objOrValue) => standardizeValue(objOrValue, key));
}

/**
 * Removes all items with fields that that match the given values.
 *
 * @param items - The items to filter.
 * @param key - The object field to check the values against.
 * @param removeValues - The values to remove if matched.
 * @return The filtered values.
 */
export function removeMatches<O, K extends keyof O>(
  items: O[],
  key: K,
  removeValues: O[K][]
): O[] {
  return items.filter((item) => !removeValues.includes(item[key]));
}

/**
 * Preserves all items with fields that that match the given values.
 *
 * @param items - The items to filter.
 * @param key - The object field to check the values against.
 * @param preserveValues - The values to preserve if matched.
 * @return The filtered values.
 */
export function preserveMatches<O, K extends keyof O>(
  items: O[],
  key: K,
  preserveValues: O[K][]
): O[] {
  return items.filter((item) => preserveValues.includes(item[key]));
}

/**
 * Collects items in an array by equivalent field values.
 *
 * @param items - The items to convert.
 * @param key  The key of the items to match on.
 * @return A collection of items keyed by their values of the given field.
 */
export function collectByField<O, K extends keyof O>(
  items: O[],
  key: K
): Record<string, O[]> {
  return items.reduce<Record<string, O[]>>(
    (acc, item) => ({
      ...acc,
      [String(item[key])]: [...(acc[String(item[key])] || []), item],
    }),
    {}
  );
}

/**
 * Removes all keys in the object besides those listed.
 *
 * @param obj - The object to remove from.
 * @param keys - The keys to preserve.
 * @return A new object with only the preserved keys.
 */
export function preserveObjectKeys<O, K extends keyof O>(
  obj: O,
  keys: K[]
): Pick<O, K> {
  return Object.entries(obj as Record<string, unknown>)
    .filter(([key]) => (keys as string[]).includes(key))
    .reduce((acc, cur) => ({ ...acc, ...cur }), {} as O);
}
