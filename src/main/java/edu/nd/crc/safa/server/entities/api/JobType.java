package edu.nd.crc.safa.server.entities.api;

/**
 * Enumerates all the possible types of jobs.
 */
public enum JobType {

    PROJECT_CREATION {
        public String toString() {
            return "PROJECT_CREATION";
        }
    },
    PROJECT_SYNC {
        public String toString() {
            return "PROJECT_SYNC";
        }
    },
    GENERATE_LINKS {
        public String toString() {
            return "GENERATE_LINKS";
        }
    },
    TRAIN_MODEL {
        public String toString() {
            return "GENERATE_LINKS";
        }
    }
}
