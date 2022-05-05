package edu.nd.crc.safa.server.entities.api;

import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.server.services.JobService;
import edu.nd.crc.safa.server.services.NotificationService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

public class ProjectCreationWorker extends JobWorker {


    /**
     * The project version of the
     */
    ProjectCommit projectCommit;

    /**
     * The entities created during job.
     */
    ProjectEntities projectEntities;

    /**
     * Service used to commit artifacts and traces.
     */
    EntityVersionService entityVersionService;

    /**
     * Service used to retrieve all created entities.
     */
    AppEntityRetrievalService appEntityRetrievalService;

    public ProjectCreationWorker(Job job,
                                 ProjectCommit projectCommit,
                                 JobService jobService,
                                 NotificationService notificationService,
                                 EntityVersionService entityVersionService,
                                 AppEntityRetrievalService appEntityRetrievalService) {
        super(job, jobService, notificationService);
        this.projectCommit = projectCommit;
        this.entityVersionService = entityVersionService;
        this.appEntityRetrievalService = appEntityRetrievalService;
    }

    public void step1CreateArtifacts() throws SafaError {
        this.entityVersionService.setArtifactsAtVersionAndSaveErrors(
            projectCommit.getCommitVersion(),
            projectCommit.getArtifacts().getAdded());
    }

    public void step2CreateTraces() throws SafaError {
        this.entityVersionService.setTracesAtVersionAndSaveErrors(
            projectCommit.getCommitVersion(),
            projectCommit.getTraces().getAdded());
    }

    public void step3RetrieveProject() {
        this.projectEntities = appEntityRetrievalService.retrieveProjectEntitiesAtProjectVersion(
            projectCommit.getCommitVersion()
        );
    }
}
