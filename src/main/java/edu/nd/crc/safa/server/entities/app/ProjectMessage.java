package edu.nd.crc.safa.server.entities.app;

/**
 * Responsible for enumerating all the possible messages for
 * updating project metadata.
 */
public enum ProjectMessage {
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
