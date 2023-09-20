import {
  MemberEntitySchema,
  MembershipSchema,
  MinimalProps,
  OpenableProps,
} from "@/types";

/**
 * The props for inputs to invite a new member to a project.
 */
export interface InviteMemberInputsProps {
  /**
   * The email to invite.
   */
  email?: string | null;
  /**
   * The entity to invite the member to.
   */
  entity: MemberEntitySchema;
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
   * The member to edit, setting edit mode.
   */
  member: MembershipSchema;
}

/**
 * The props for displaying a table of members.
 */
export interface MemberTableProps extends MinimalProps {
  /**
   * The type of entities in this table.
   */
  entity: MemberEntitySchema;
}
