package edu.nd.crc.safa.server.entities.api.layout;

import java.util.List;

import lombok.Data;

/**
 * Rule in project creating warnings over artifacts.
 */
@Data
public class RuleAppEntity {
    /**
     * The condition which to match the source
     * and target types.
     */
    RuleCondition condition;
    /**
     * The number expected for the condition to be true.
     */
    int value;
    /**
     * The source artifact type to apply the condition to.
     */
    String sourceType;
    /**
     * The target artifact type being applied in condition.
     */
    String targetType;
    /**
     * The list of sub-rules joined by condition
     * (e.g. AND or OR)
     */
    List<RuleAppEntity> subRules;
}
