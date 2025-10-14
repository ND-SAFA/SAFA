import { Message, Subscription } from "webstomp-client";

/**
 * A channel for stomp messages.
 */
export interface StompChannel {
  /**
   * The subscription to the channel.
   */
  subscription: Subscription;
  /**
   * The topic of the channel.
   */
  topic: string;
  /**
   * A callback for handling messages to the channel.
   */
  handler: (message: Message) => void;
}

/**
 * Notifies client of a series of changes to the project.
 *
 */
export interface ChangeMessageSchema {
  /**
   * The user initiating the change.
   */
  user: string;
  /**
   * List of changes occurring to project.
   * Each change depicts what entity was affected, how it was affected
   * (UPDATED / DELETED), and the affected entity ids).
   */
  changes: ChangeSchema[];
  /**
   * Includes whether the default document layout should be updated.
   * This is true if any artifacts or trace links where changed.
   */
  updateLayout: boolean;
}

/**
 * Entity being changed.
 */
export type EntityType =
  | "PROJECT"
  | "MEMBERS"
  | "VERSION"
  | "TYPES"
  | "TRACE_MATRICES"
  | "DOCUMENT"
  | "ARTIFACTS"
  | "TRACES"
  | "WARNINGS"
  | "JOBS"
  | "LAYOUT"
  | "SUBTREES"
  | "MODELS"
  | "ATTRIBUTES"
  | "ATTRIBUTE_LAYOUTS"
  | "ACTIVE_MEMBERS";

/**
 * Represents list of changed entities.
 */
export interface ChangeSchema {
  /**
   * The entity being changed.
   */
  entity: EntityType;
  /**
   * The action performed on the entity.
   */
  action: ActionType;
  /**
   * The ids of the entities being changed.
   */
  entityIds: string[];
  /**
   * The entities being changed themselves.
   */
  entities: object[];
}

/**
 * A list of all entities that can trigger updates
 * through notifications when made by the current user.
 */
export const notifyUserEntities: EntityType[] = [
  "VERSION",
  "WARNINGS",
  "LAYOUT",
  "TYPES",
];

/**
 * The action performed on an change to an entity.
 * Used in notifications to signal asynchronous updates.
 */
export enum ActionType {
  UPDATE = "UPDATE",
  DELETE = "DELETE",
}
