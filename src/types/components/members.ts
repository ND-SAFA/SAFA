import { MembershipSchema, MinimalProps, OpenableProps } from "@/types";

/**
 * The props for inputs to invite a new member to a project.
 */
export interface InviteMemberInputsProps {
  /**
   * The email to invite.
   */
  email?: string | null;
  /**
   * The project id to invite the member to.
   */
  projectId?: string;
}

/**
 * The props for displaying a project member save modal.
 */
export interface InviteMemberModalProps
  extends OpenableProps,
    InviteMemberInputsProps {}

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

/**
 * The props for displaying a table of members.
 */
export interface MemberTableProps extends MinimalProps {
  /**
   * The type of members being managed.
   */
  variant: "project" | "team" | "organization";
}
