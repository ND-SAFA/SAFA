package edu.nd.crc.safa.server.entities.app;

/**
 * Responsible for enumerating all the possible entities that can
 * be updated via notifications.
 */
public enum ProjectEntityTypes {
    DOCUMENTS {
        public String toString() {
            return "DOCUMENTS";
        }
    },
    MEMBERS {
        public String toString() {
            return "MEMBERS";
        }
    }
}
