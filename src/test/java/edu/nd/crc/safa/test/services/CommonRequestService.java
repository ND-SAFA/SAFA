package edu.nd.crc.safa.test.services;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.requests.SafaRequest;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class CommonRequestService {
    ServiceProvider serviceProvider;

    public static List<JobAppEntity> getUserJobs() throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Jobs.Meta.GET_USER_JOBS)
            .getAsArray(JobAppEntity.class);
    }

    public static List<JobAppEntity> getProjectJobs(Project project) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Jobs.Meta.GET_PROJECT_JOBS)
            .withProject(project)
            .getAsArray(JobAppEntity.class);
    }
}
