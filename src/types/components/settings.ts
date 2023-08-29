import { MembershipSchema, OpenableProps } from "@/types";

/**
 * The types of tabs on the settings page.
 */
export enum SettingsTabTypes {
  members = "members",
  upload = "upload",
  integrations = "integrations",
  attributes = "attributes",
}

/**
 * The props for displaying a project member save modal.
 */
export interface ProjectMemberModalProps extends OpenableProps {
  /**
   * The member to edit, setting edit mode.
   */
  member?: MembershipSchema;
  /**
   * The email to invite, setting add mode.
   */
  email?: string | null;
  /**
   * The project id to invite the member to, if in add mode.
   */
  projectId?: string;
}

/**
 * The props for inputs to invite a new member to a project.
 */
export interface InviteMemberInputsProps {
  /**
   * The email to invite, setting add mode.
   */
  email?: string | null;
  /**
   * The project id to invite the member to, if in add mode.
   */
  projectId?: string;
}

/**
 * The props for displaying a project member edit role button.
 */
export interface MemberRoleButtonProps {
  /**
   * The project id to edit the member of.
   */
  projectId: string;
  /**
   * The member to edit, setting edit mode.
   */
  member: MembershipSchema;
}
