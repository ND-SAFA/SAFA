package edu.nd.crc.safa.features.rules.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Rule in project creating warnings over artifacts.
 */
@Data
@AllArgsConstructor
public class RuleAppEntity {
    /**
     * UUID uniquely identifying rule.
     */
    private String id;
    /**
     * The name of the rule.
     */
    private String name;
    /**
     * Description of what the rule is doing.
     */
    private String description;
    /**
     * The condition which to match the source
     * and target types.
     */
    private RuleCondition condition;
    /**
     * The number expected for the condition to be true.
     */
    private int value = 1;
    /**
     * The source artifact type to apply the condition to.
     */
    private String sourceType;
    /**
     * How the source and target types should be related.
     */
    private RuleRelation relation;
    /**
     * The target artifact type being applied in condition.
     */
    private String targetType;
    /**
     * The list of sub-rules joined by condition
     * (e.g. AND or OR)
     */
    private List<RuleAppEntity> subRules;

    public String toString() {
        if (!subRules.isEmpty()) {
            return this.subRules
                .stream()
                .map(RuleAppEntity::toString)
                .collect(Collectors.joining(this.condition.toString()));
        } else {
            if (RuleCondition.containsVariable(condition)) {
                String format = "%s(" + createFormattedArguments(4) + ")";
                return String.format(
                    format,
                    condition.toString(),
                    value,
                    sourceType,
                    relation,
                    targetType);
            }
            String format = "%s(" + createFormattedArguments(4) + ")";
            return String.format(
                format,
                condition.toString(),
                sourceType,
                relation,
                targetType);
        }
    }

    private String createFormattedArguments(int n) {
        List<String> arguments = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            arguments.add("%s");
        }
        return String.join(",", arguments);
    }
}
