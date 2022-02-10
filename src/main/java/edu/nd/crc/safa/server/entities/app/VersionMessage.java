package edu.nd.crc.safa.server.entities.app;

/**
 * Responsible for enumerating all the possible messages for
 * updating versioned entities.
 */
public enum VersionMessage {
    VERSION {
        public String toString() {
            return "VERSION";
        }
    },
    ARTIFACTS {
        public String toString() {
            return "ARTIFACTS";
        }
    },
    TRACES {
        public String toString() {
            return "TRACES";
        }
    }
}
