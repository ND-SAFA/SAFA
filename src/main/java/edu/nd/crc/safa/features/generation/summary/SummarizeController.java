package edu.nd.crc.safa.features.generation.summary;

import java.util.List;
import javax.validation.Valid;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides summarization endpoints.
 */
@RestController
public class SummarizeController extends BaseController {
    public SummarizeController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Performs summary request.
     *
     * @param request Defines content to summarize and model to do it with.
     * @return List of summaries.
     */
    @PostMapping(AppRoutes.Summarize.SUMMARIZE_ARTIFACTS)
    public List<String> summarizeArtifacts(@RequestBody @Valid SummarizeRequestDTO request) {
        return serviceProvider.getSummaryService().generateSummaries(request);
    }
}
