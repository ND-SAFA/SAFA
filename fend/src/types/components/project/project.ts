import {
  DisabledProps,
  MinimalProps,
  OpenableProps,
  ProjectIdProps,
} from "@/types";

/**
 * The props for displaying a project files upload input.
 */
export interface ProjectFilesInputProps {
  /**
   * The value of the input.
   */
  modelValue: File[];
  /**
   * The test selector for the input.
   */
  dataCy?: string;
}

/**
 * The props to display a project's identifying information.
 */
export interface ProjectIdentifierProps {
  /**
   * The name of the project.
   */
  name: string;
  /**
   * The description of the project.
   */
  description: string;
  /**
   * Whether a project is being updated, rather than created.
   */
  isUpdate?: boolean;
  /**
   * The test selector for the name.
   */
  dataCyName?: string;
  /**
   * The test selector for the description.
   */
  dataCyDescription?: string;
}

/**
 * The props for displaying a project's version creator.
 */
export interface CreateVersionModalProps
  extends OpenableProps,
    Partial<ProjectIdProps> {}

/**
 * The props for displaying a project table.
 */
export interface ProjectSelectorTableProps extends OpenableProps, MinimalProps {
  /**
   * If true, only projects for the current team will be displayed.
   */
  teamOnly?: boolean;
}

/**
 * The props for displaying a project version table.
 */
export interface VersionSelectorTableProps
  extends OpenableProps,
    MinimalProps,
    DisabledProps,
    ProjectIdProps {
  /**
   * If true, the current version will be hidden.
   */
  hideCurrentVersion?: boolean;
}
