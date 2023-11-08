package edu.nd.crc.safa.features.generation.prompt;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for completing prompts.
 */
@RestController
public class CompletionController extends BaseController {
    public CompletionController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Completes the prompt for given model
     *
     * @param request The request payload defining prompt and model.
     * @return The completion.
     */
    @PostMapping(AppRoutes.Prompts.COMPLETE)
    public PromptResponse completePrompt(@RequestBody @Valid TGenPromptRequest request) {
        return getServiceProvider().getGenApi().generatePrompt(request);
    }
}
