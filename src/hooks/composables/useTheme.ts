import { computed } from "vue";
import { useTheme as useVuetifyTheme, ThemeInstance } from "vuetify";
import { LocalStorageKeys, ThemeHook } from "@/types";

export function useTheme(): ThemeHook<ThemeInstance> {
  const theme = useVuetifyTheme();
  const darkMode = computed(() => theme.global.current.value.dark);

  function toggleDarkMode(): void {
    const mode = theme.global.current.value.dark ? "light" : "dark";

    theme.global.name.value = mode;
    localStorage.setItem(LocalStorageKeys.darkMode, mode);
  }

  return {
    theme,
    darkMode,
    toggleDarkMode,
  };
}
