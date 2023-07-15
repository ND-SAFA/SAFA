package edu.nd.crc.safa.features.generation.prompt;

import javax.validation.Valid;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.tgen.TGen;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for completing prompts.
 */
@RestController
public class PromptController extends BaseController {
    public PromptController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Completes the prompt for given model
     *
     * @param request            The request payload defining prompt and model.
     * @param safaRequestBuilder The request builder used for sending prompt requtest to TGEN.
     * @return The completion.
     */
    @PostMapping(AppRoutes.Prompts.COMPLETE)
    public TGenPromptResponse completePrompt(@RequestBody @Valid TGenPromptRequest request,
                                             @Autowired SafaRequestBuilder safaRequestBuilder) {
        TGen controller = new TGen(safaRequestBuilder);
        return controller.generatePrompt(request);
    }
}
