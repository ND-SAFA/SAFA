/**
 * Represents the project TIM file format.
 */
export type TimJsonSchema = {
  DataFiles: {
    [artifactType: string]: {
      File: string;
    };
  };
} & {
  [traceType: string]: {
    Source: string;
    Target: string;
    File: string;
  };
};
