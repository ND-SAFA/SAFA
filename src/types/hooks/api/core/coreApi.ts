import { ComputedRef, Ref } from "vue";
import { IOHandlerCallback } from "@/types/api";

/**
 * Configuration details for a api request.
 */
export interface RequestConfig<T> extends IOHandlerCallback<T> {
  /**
   * A message to display on success.
   */
  success?: string;
  /**
   * A message to display on error.
   */
  error?: string;
  /**
   * Whether to use the app loading state.
   */
  useAppLoad?: boolean;
}

/**
 * A hook for calling API endpoints.
 */
export interface ApiHook {
  /**
   * Whether this request manager is loading a request.
   */
  loading: Ref<boolean>;
  /**
   * Whether the most recent request had an error.
   */
  error: Ref<boolean>;
  /**
   * Resets the API state.
   */
  handleReset(): void;
  /**
   * Creates a reactive error message for inputs.
   * @param message - The message to display.
   */
  errorMessage(message: string): ComputedRef<string | false>;
  /**
   * Runs a request and handles the loading and error states,
   * as well as optionally reporting success and error messages.
   *
   * @param cb - The callback to run.
   * @param config - The callbacks and messages to display on success and error.
   */
  handleRequest<T = void>(
    cb: () => Promise<T>,
    config?: RequestConfig<T>
  ): Promise<T | undefined>;
}
