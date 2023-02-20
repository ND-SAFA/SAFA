import { computed, ComputedRef } from "vue";
import { MarginProps, SizeType } from "@/types";

const convertMargin = (value: SizeType) => {
  switch (value) {
    case "":
      return "none";
    case "1":
      return "xs";
    case "2":
      return "sm";
    case "3":
      return "md";
    case "4":
      return "lg";
    case "5":
    default:
      return "xl";
  }
};

/**
 * Creates a classname based on margin props.
 * @param props - The margins to include.
 * @return The computed class name.
 */
export function useMargins(props: MarginProps): ComputedRef<string> {
  return computed(() => {
    let classNames = "";

    if (props.x) classNames += ` q-mx-${convertMargin(props.x)}`;
    if (props.l) classNames += ` q-ml-${convertMargin(props.l)}`;
    if (props.r) classNames += ` q-mr-${convertMargin(props.r)}`;
    if (props.y) classNames += ` q-my-${convertMargin(props.y)}`;
    if (props.t) classNames += ` q-mt-${convertMargin(props.t)}`;
    if (props.b) classNames += ` q-mb-${convertMargin(props.b)}`;

    return classNames;
  });
}
