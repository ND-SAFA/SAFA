import { computed, ComputedRef, ref, watch } from "vue";
import { defineStore } from "pinia";
import { pinia } from "@/plugins";

/**
 * The properties for the time display.
 */
interface TimeDisplayProps {
  /**
   * The start of the duration, as an ISO timestamp.
   */
  getStart: () => string;
  /**
   * The end of the duration, as an ISO timestamp.
   * Set as empty string to display the current time.
   */
  getEnd: () => string;
}

/**
 * A hook for managing the display of a timestamp that updates in real-time.
 */
interface TimeDisplayHook {
  /**
   * The current time.
   */
  displayTime: ComputedRef<string>;
  /**
   * Updates the time display manually.
   */
  resetTime(): void;
  /**
   * Stops the time display from updating.
   */
  stopTime(): void;
}

/**
 * The interval for updating the time display, in milliseconds.
 */
const interval = 60000;

/**
 * A store for managing the current time.
 * Watches for updates to time in a single place, at 1-minute intervals.
 */
const useTime = defineStore("time", () => {
  const now = ref(new Date(Date.now()).getTime());
  const timer = ref<ReturnType<typeof setTimeout> | null>(null);

  function updateNow(repeat = true) {
    now.value = new Date(Date.now()).getTime();

    if (repeat) {
      if (timer.value) {
        clearTimeout(timer.value);
      }
      timer.value = setTimeout(updateNow, interval);
    }
  }

  updateNow(true);

  return {
    now,
    at(timestamp: string) {
      return new Date(timestamp).getTime();
    },
  };
});

const timeStore = useTime(pinia);

/**
 * A hook for managing the display of a timestamp that updates in real-time.
 * @param props - The start and end of the duration.
 * @return The time display and methods to control it.
 */
export function useTimeDisplay(props: TimeDisplayProps): TimeDisplayHook {
  const repeat = ref(true);

  function getCurrentEndTime() {
    return props.getEnd() ? timeStore.at(props.getEnd()) : timeStore.now;
  }

  const startTime = computed(() =>
    props.getStart() ? timeStore.at(props.getStart()) : timeStore.now
  );
  const endTime = ref(getCurrentEndTime());

  const displayTime = computed(() => {
    if (!props.getStart()) {
      repeat.value = false;
      return "";
    }

    const duration = Math.max(endTime.value - startTime.value, 0);
    const hours = Math.floor(duration / 3600000);
    const minutes = Math.floor((duration % 3600000) / 60000);
    const hoursDisplay = `${hours} Hour${hours === 1 ? "" : "s"}`;
    const minutesDisplay = `${minutes} Minute${minutes === 1 ? "" : "s"}`;

    repeat.value = !props.getEnd();

    return hours ? `${hoursDisplay}, ${minutesDisplay}` : minutesDisplay;
  });

  watch(
    () => timeStore.now,
    () => {
      if (!repeat.value) return;

      endTime.value = getCurrentEndTime();
    }
  );

  return {
    displayTime,
    resetTime() {
      endTime.value = getCurrentEndTime();
    },
    stopTime() {
      repeat.value = false;
    },
  };
}
