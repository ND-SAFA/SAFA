import { MessageType } from "@/types";

/**
 * The props for the Alert component.
 */
export interface AlertProps {
  /**
   * The type of alert to render.
   */
  type?: MessageType;
  /**
   * The message to render.
   */
  message?: string;
}
