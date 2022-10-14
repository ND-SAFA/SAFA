/**
 * Represents the project TIM file format.
 */
export type TimModel = {
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
