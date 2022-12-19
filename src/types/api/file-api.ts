/**
 * Represents the project TIM file format.
 */
export type TimSchema = {
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
