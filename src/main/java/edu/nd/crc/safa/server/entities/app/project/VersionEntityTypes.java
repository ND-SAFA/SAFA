package edu.nd.crc.safa.server.entities.app.project;

/**
 * Responsible for enumerating all the possible versioned entities
 * that can be updated via notifications.
 */
public enum VersionEntityTypes {
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
    },
    WARNINGS {
        public String toString() {
            return "WARNINGS";
        }
    }
}
