package edu.nd.crc.safa.features.permissions.checks.config;

/**
 * Checks that the project involved is smaller than the limit specified in the configuration
 */
public class MaxProjectSizeCheck extends IntConfigurationComparisonCheck {
    public MaxProjectSizeCheck() {
        super(context -> 1  /* TODO */, "limits.max_project_size", ComparisonType.LESS_OR_EQUAL);
    }
}
