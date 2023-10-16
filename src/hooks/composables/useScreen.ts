import { computed } from "vue";
import { useQuasar } from "quasar";
import { ScreenHook } from "@/types";

/**
 * A hook for managing changes with the screen size.
 */
export function useScreen(): ScreenHook {
  const $q = useQuasar();

  const screen = computed(() => $q.screen);

  const smallWindow = computed(() => $q.screen.lt.md);

  return {
    screen,
    smallWindow,
  };
}
