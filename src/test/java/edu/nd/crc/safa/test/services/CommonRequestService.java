package edu.nd.crc.safa.test.services;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.generation.prompt.PromptResponse;
import edu.nd.crc.safa.features.generation.prompt.TGenPromptRequest;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.requests.SafaRequest;

import lombok.AllArgsConstructor;
import org.json.JSONObject;


@AllArgsConstructor
public class CommonRequestService {
    ServiceProvider serviceProvider;
    Gen gen;

    public static class Project {
        public static List<JobAppEntity> getUserJobs() throws Exception {
            return SafaRequest
                .withRoute(AppRoutes.Jobs.Meta.GET_USER_JOBS)
                .getAsArray(JobAppEntity.class);
        }

        public static List<JobAppEntity> getProjectJobs(edu.nd.crc.safa.features.projects.entities.db.Project project) throws Exception {
            return SafaRequest
                .withRoute(AppRoutes.Jobs.Meta.GET_PROJECT_JOBS)
                .withProject(project)
                .getAsArray(JobAppEntity.class);
        }

        public static List<TraceAppEntity> getGeneratedLinks(ProjectVersion projectVersion) throws Exception {
            return SafaRequest
                .withRoute(AppRoutes.Links.GET_GENERATED_LINKS_IN_PROJECT_VERSION)
                .withVersion(projectVersion)
                .getAsArray(TraceAppEntity.class);
        }
    }

    public static class Gen {
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

        public static JobAppEntity performHGen(ProjectVersion projectVersion, HGenRequest request) throws Exception {
            return SafaRequest
                .withRoute(AppRoutes.HGen.GENERATE)
                .withVersion(projectVersion)
                .postWithJsonObject(request, JobAppEntity.class);
        }

        public static JobAppEntity performTGen(TGenRequestAppEntity request) throws Exception {
            return SafaRequest
                .withRoute(AppRoutes.Jobs.Traces.GENERATE)
                .postWithJsonObject(request, JobAppEntity.class);
        }
    }
}
