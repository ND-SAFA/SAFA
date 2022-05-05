package edu.nd.crc.safa.server.entities.api.jobs;

/**
 * Enumerates all the possible types of jobs.
 */
public enum JobType {
    FLAT_FILE_PROJECT_CREATION {
        public String toString() {
            return "FLAT_FILE_PROJECT_CREATION";
        }
    },
    JIRA_PROJECT_CREATION {
        public String toString() {
            return "JIRA_PROJECT_CREATION";
        }
    },
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
