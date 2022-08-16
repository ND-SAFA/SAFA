package edu.nd.crc.safa.features.delta.entities.db;

import java.io.Serializable;

import lombok.AllArgsConstructor;

/**
 * The types of modifications possible for a project entity.
 */
@AllArgsConstructor
public enum ModificationType implements Serializable {
    ADDED("ADDED"),
    MODIFIED("MODIFIED"),
    REMOVED("REMOVED"),
    NO_MODIFICATION("NO_MODIFICATION");

    private String value;

    @Override
    public String toString() {
        return this.value;
    }
}
