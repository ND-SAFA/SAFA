package edu.nd.crc.safa.features.permissions.checks.config;

import java.util.function.Function;

import edu.nd.crc.safa.features.generation.summary.SummarizeArtifactRequestDTO;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

/**
 * Checks that the project involved is smaller than the limit specified in the configuration
 */
public class SummarizationMaxProjectSizeCheck extends IntConfigurationComparisonCheck {
    public SummarizationMaxProjectSizeCheck() {
        this(context -> context.getProjectStatistics().getUnsummarizedCodeArtifactsTotal());
    }

    public SummarizationMaxProjectSizeCheck(SummarizeArtifactRequestDTO summarizationRequest) {
        this(context -> summarizationRequest.getArtifacts().size());
    }

    public SummarizationMaxProjectSizeCheck(Function<PermissionCheckContext, Integer> getTotalSummarizedFunction) {
        super(getTotalSummarizedFunction, "limits.summarization_max_project_size", ComparisonType.LESS_OR_EQUAL);
    }

    @Override
    public String getMessage() {
        return "Project must have at most " + getCachedCompareValue() + " artifacts";
    }

    @Override
    public boolean superuserCanOverride() {
        return true;
    }
}
