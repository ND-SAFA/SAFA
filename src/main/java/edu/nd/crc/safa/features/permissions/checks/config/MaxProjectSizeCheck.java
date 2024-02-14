package edu.nd.crc.safa.features.permissions.checks.config;

/**
 * Checks that the project involved is smaller than the limit specified in the configuration
 */
public class MaxProjectSizeCheck extends IntConfigurationComparisonCheck {
    public MaxProjectSizeCheck() {
        super(context -> context.getProjectStatistics().getArtifactsTotal(),
            "limits.max_project_size", ComparisonType.LESS_OR_EQUAL);
    }

    @Override
    public String getMessage() {
        return "Project must have at most " + getCachedCompareValue() + " artifacts";
    }
}
