package edu.nd.crc.safa.server.entities.api.layout;

import lombok.AllArgsConstructor;

/**
 * Enumerates the types of relationships
 * to use in rules.
 */
@AllArgsConstructor
public enum RuleRelation {

    CHILD("CHILD"),
    SIBLING("SIBLING");

    private final String value;

    @Override
    public String toString() {
        return value;
    }
}
