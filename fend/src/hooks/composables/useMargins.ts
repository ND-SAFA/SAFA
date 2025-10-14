import { ComputedRef } from "vue";
import { MarginProps, SizeType } from "@/types";
import { useClasses } from "@/hooks";

const convertMargin = (value?: SizeType) => {
  switch (value) {
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
 * @param classes - Additional classes to include besides the margins classes.
 * @return The computed class name.
 */
export function useMargins<T extends Partial<MarginProps>>(
  props: T,
  classes: () => [keyof T | boolean, string | undefined][] = () => []
): ComputedRef<string> {
  return useClasses(props, () => [
    ["x", ` q-mx-${convertMargin(props.x)}`],
    ["y", ` q-my-${convertMargin(props.y)}`],
    ["l", ` q-ml-${convertMargin(props.l)}`],
    ["r", ` q-mr-${convertMargin(props.r)}`],
    ["t", ` q-mt-${convertMargin(props.t)}`],
    ["b", ` q-mb-${convertMargin(props.b)}`],
    ...classes(),
  ]);
}
