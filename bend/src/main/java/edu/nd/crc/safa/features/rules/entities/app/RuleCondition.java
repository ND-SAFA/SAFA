package edu.nd.crc.safa.features.rules.entities.app;

import lombok.AllArgsConstructor;

/**
 * Enumerates the list of available conditions to match on.
 */
@AllArgsConstructor
public enum RuleCondition {

    AT_LEAST_ONE("at-least-one"),
    AT_LEAST_N("at-least-n"),
    EXACTLY_ONE("exactly-one"),
    EXACTLY_N("exactly-n"),
    LESS_THAN_N("less-than-n"),
    AND("&&"),
    OR("||");

    private final String value;

    public static boolean containsVariable(RuleCondition ruleCondition) {
        return ruleCondition.value.contains("-n");
    }

    @Override
    public String toString() {
        return value;
    }
}
