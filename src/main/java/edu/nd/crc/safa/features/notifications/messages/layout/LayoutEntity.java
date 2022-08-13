package edu.nd.crc.safa.features.notifications.messages.layout;

import lombok.AllArgsConstructor;

/**
 * Enumerates entities that contains layouts.
 */
@AllArgsConstructor
public enum LayoutEntity {
    /**
     * Signifies that entire layout has been generated or default document has been affected.
     */
    PROJECT,
    /**
     * Signifies that document specified had its layout updated.
     */
    DOCUMENT;

    @Override
    public String toString() {
        return this.name();
    }
}
