import { computed, getCurrentInstance, WritableComputedRef } from "vue";

/**
 * Synchronizes a v-model value.
 * @param props - The component props.
 * @param propName - The prop to synchronize with.
 * @emits `update:{propName}` - When the model value is set.
 */
export function useVModel<T extends Record<string, unknown>, K extends keyof T>(
  props: T,
  propName: K
): WritableComputedRef<T[K]> {
  const vm = getCurrentInstance()?.proxy;

  return computed({
    get() {
      return props[propName];
    },
    set(value) {
      vm?.$emit(`update:${String(propName)}`, value);
    },
  });
}
