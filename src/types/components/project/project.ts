import { MinimalProps, OpenableProps, ProjectIdProps } from "@/types";

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
export interface ProjectSelectorTableProps
  extends OpenableProps,
    MinimalProps {}

/**
 * The props for displaying a project version table.
 */
export interface VersionSelectorTableProps
  extends OpenableProps,
    MinimalProps,
    ProjectIdProps {
  /**
   * If true, the current version will be hidden.
   */
  hideCurrentVersion?: boolean;
}
