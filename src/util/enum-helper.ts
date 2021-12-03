/**
 * Returns the enum keys if they are strings.
 * @param myEnum
 */
export function getEnumKeys(myEnum: any): string[] {
  return Object.keys(myEnum)
    .map((key) => myEnum[key])
    .filter((value) => typeof value === "string") as string[];
}
