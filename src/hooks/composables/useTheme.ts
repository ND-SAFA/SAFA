import { computed } from "vue";
import { setCssVar, useQuasar } from "quasar";
import { LocalStorageKeys, ThemeHook } from "@/types";
import { darkPalette, lightPalette } from "@/util";

export function useTheme(): ThemeHook {
  const $q = useQuasar();

  const darkMode = computed({
    get: () => $q.dark.isActive,
    set: (dark) => $q.dark.set(dark),
  });

  function setTheme(): void {
    const theme = darkMode.value ? darkPalette : lightPalette;

    Object.entries(theme).forEach(([key, color]) => {
      setCssVar(key, color);
    });
  }

  function toggleDarkMode(mode?: boolean): void {
    if (mode === undefined) {
      mode = !darkMode.value;
    }

    darkMode.value = mode;
    localStorage.setItem(LocalStorageKeys.darkMode, String(mode));
    setTheme();
  }

  return {
    theme: $q,
    darkMode,
    toggleDarkMode,
  };
}
