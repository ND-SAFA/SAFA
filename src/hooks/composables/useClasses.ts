import { computed, ComputedRef } from "vue";

/**
 * Creates a classname based on the given props.
 * @param props - The props to check the existence of.
 * @param classes - A list of key-value pairs, where if they key is truthy in the props, the
 * value will be included in the classname.
 * @return The computed class name.
 */
export function useClasses<T>(
  props: T,
  classes: () => [keyof T | boolean, string | undefined][]
): ComputedRef<string> {
  return computed(() => {
    const classNames: string[] = [];

    classes().forEach(([key, value]) => {
      const keyIsValid = typeof key === "string" ? !!props[key] : key;

      if (!keyIsValid || !value) return;

      classNames.push(value);
    });

    return classNames.join(" ");
  });
}
