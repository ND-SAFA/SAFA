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

  function loadDarkMode(): void {
    const storedDarkMode =
      localStorage.getItem(LocalStorageKeys.darkMode) || "";
    const darkMode =
      (
        {
          true: true,
          false: false,
          auto: "auto",
        } as Record<string, boolean | "auto">
      )[storedDarkMode] || "auto";

    toggleDarkMode(darkMode);
  }

  function toggleDarkMode(mode?: boolean | "auto"): void {
    const now = new Date();
    const hour = now.getHours();
    const isNight = hour < 6 || hour >= 18; // Assuming night is from 6PM to 6AM

    if (mode === undefined) {
      mode = !darkMode.value;
    }

    darkMode.value = typeof mode === "boolean" ? mode : isNight;
    localStorage.setItem(LocalStorageKeys.darkMode, String(mode));
    setTheme();
  }

  return {
    theme: $q,
    darkMode,
    loadDarkMode,
    toggleDarkMode,
  };
}
