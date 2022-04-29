package edu.nd.crc.safa.server.entities.app.project;

/**
 * Enumerates the types of nodes used in a safety case
 */
public enum SafetyCaseType {
    SOLUTION {
        public String toString() {
            return "SOLUTION";
        }
    },
    CONTEXT {
        public String toString() {
            return "CONTEXT";
        }
    },
    GOAL {
        public String toString() {
            return "GOAL";
        }
    },
    STRATEGY {
        public String toString() {
            return "STRATEGY";
        }
    }
}
