package edu.nd.crc.safa.server.entities.api.layout;

/**
 * Enumerates the list of available conditions to match on.
 */
public enum RuleCondition {
    AT_LEAST_ONE {
        public String toString() {
            return "at-least-one";
        }
    },
    AT_LEAST_N {
        public String toString() {
            return "at-least-n";
        }
    },
    EXACTLY_ONE {
        public String toString() {
            return "exactly-one";
        }
    },
    EXACTLY_N {
        public String toString() {
            return "exactly-n";
        }
    },
    LESS_THAN_N {
        public String toString() {
            return "less-than-n";
        }
    },
    AND {
        public String toString() {
            return "&&";
        }
    },
    OR {
        public String toString() {
            return "||";
        }
    };

    public static boolean containsVariable(RuleCondition ruleCondition) {
        return ruleCondition.toString().contains("-n");
    }
}
