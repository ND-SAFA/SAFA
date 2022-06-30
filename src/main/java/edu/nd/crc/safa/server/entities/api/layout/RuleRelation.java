package edu.nd.crc.safa.server.entities.api.layout;

/**
 * Enumerates the types of relationships
 * to use in rules.
 */
public enum RuleRelation {
    CHILD {
        public String toString() {
            return "CHILD";
        }
    }, SIBLING {
        public String toString() {
            return "SIBLING";
        }
    }
}
