import { LoadingProps, TestableProps } from "@/types";

/**
 * The props for the modal displaying errors.
 */
export interface ErrorModalProps {
  /**
   * The errors to display.
   */
  errors: string[];
}

/**
 * The props for displaying a modal.
 */
export interface ModalProps extends LoadingProps, TestableProps {
  /**
   * The modal title.
   */
  title: string;
  /**
   * The modal subtitle.
   */
  subtitle?: string;
  /**
   * Whether the modal is open.
   */
  open: boolean;
  /**
   * A fixed width size to set for the modal.
   */
  size?: "sm" | "md" | "lg" | "xl";
}
