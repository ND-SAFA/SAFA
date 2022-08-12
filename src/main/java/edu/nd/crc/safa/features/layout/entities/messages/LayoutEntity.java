package edu.nd.crc.safa.features.layout.entities.messages;

import lombok.AllArgsConstructor;

/**
 * Enumerates entities that contains layouts.
 */
@AllArgsConstructor
public enum LayoutEntity {
    /**
     * Signifies that entire layout has been generated or default document has been affected.
     */
    PROJECT("PROJECT"),
    /**
     * Signifies that document specified had its layout updated.
     */
    DOCUMENT("DOCUMENT");

    private String value;

    @Override
    public String toString() {
        return this.value;
    }
}
