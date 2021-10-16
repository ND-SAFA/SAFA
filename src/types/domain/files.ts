export interface Resource {
  file: string;
}
export interface TraceMatrixFile extends Resource {
  source: string;
  target: string;
}

export interface DataFile {
  [key: string]: Resource;
}

export interface TimFile {
  [key: string]: DataFile | TraceMatrixFile;
}
