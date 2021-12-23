/**
 * Returns whether the two given arrays have equal item values.
 *
 * @param array1 - The first array.
 * @param array2 - The second array.
 *
 * @return Whether the two arrays have equal item values.
 */
export function areArraysEqual(
  array1: (number | string)[],
  array2: (number | string)[]
): boolean {
  return (
    array1.length === array2.length &&
    array1.every((value, index) => value === array2[index])
  );
}
