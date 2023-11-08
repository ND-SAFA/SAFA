package edu.nd.crc.safa.test.services.requests;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.generation.prompt.PromptResponse;
import edu.nd.crc.safa.features.generation.prompt.TGenPromptRequest;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;

public class GenCommonRequests {
    public static JobAppEntity performProjectSummary(ProjectVersion projectVersion) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Summarize.SUMMARIZE_PROJECT)
            .withVersion(projectVersion)
            .postWithJsonObject(new JSONObject(), JobAppEntity.class);
    }

    public static PromptResponse completePrompt(TGenPromptRequest request) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Prompts.COMPLETE)
            .postWithJsonObject(request, PromptResponse.class);
    }

    public JobAppEntity performHGen(ProjectVersion projectVersion, HGenRequest request) {
        return SafaRequest
            .withRoute(AppRoutes.HGen.GENERATE)
            .withVersion(projectVersion)
            .postWithJsonObject(request, JobAppEntity.class);
    }

    public JobAppEntity performTGen(TGenRequestAppEntity request) {
        return SafaRequest
            .withRoute(AppRoutes.Jobs.Traces.GENERATE)
            .postWithJsonObject(request, JobAppEntity.class);
    }
}
