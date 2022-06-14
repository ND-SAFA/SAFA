package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.layout.CreateLayoutJob;
import edu.nd.crc.safa.layout.KlayLayoutGenerator;
import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.api.jobs.JobType;
import edu.nd.crc.safa.server.entities.app.JobAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;
import edu.nd.crc.safa.server.services.ServiceProvider;
import edu.nd.crc.safa.server.services.jobs.JobService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.javatuples.Pair;
import org.springframework.batch.core.JobParametersInvalidException;
import org.springframework.batch.core.repository.JobExecutionAlreadyRunningException;
import org.springframework.batch.core.repository.JobInstanceAlreadyCompleteException;
import org.springframework.batch.core.repository.JobRestartException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for:
 * - generating the layout of a document
 * - saving position of an artifact
 */
@RestController
public class LayoutController extends BaseController {

    DocumentRepository documentRepository;

    JobService jobService;
    AppEntityRetrievalService appEntityRetrievalService;
    ServiceProvider serviceProvider;

    @Autowired
    public LayoutController(ResourceBuilder resourceBuilder,
                            DocumentRepository documentRepository,
                            JobService jobService,
                            AppEntityRetrievalService appEntityRetrievalService,
                            ServiceProvider serviceProvider) {
        super(resourceBuilder);
        this.documentRepository = documentRepository;
        this.jobService = jobService;
        this.appEntityRetrievalService = appEntityRetrievalService;
        this.serviceProvider = serviceProvider;
    }

    //TODO: Add unit tests
    @PostMapping(AppRoutes.Projects.Layout.createLayoutForProject)
    public Map<String, LayoutPosition> createLayoutForProject(@PathVariable UUID versionId) {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();

        String name = createJobName("project", projectVersion);
        // TODO : JobDbEntity jobDbEntity = jobService.createNewJob(JobType.GENERATE_LAYOUT, name);

        ProjectAppEntity projectAppEntity =
            appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(projectVersion);

        KlayLayoutGenerator layoutGenerator = new KlayLayoutGenerator(projectAppEntity.artifacts,
            projectAppEntity.traces);
        return layoutGenerator.layout();
    }

    //TODO: Add unit tests
    @PostMapping(AppRoutes.Projects.Layout.createLayoutForDocument)
    public JobAppEntity createLayoutForDocument(@PathVariable UUID versionId,
                                                @PathVariable UUID documentId) throws Exception {
        ProjectVersion projectVersion = resourceBuilder.fetchVersion(versionId).withEditVersion();
        Document document = getDocumentById(documentRepository, documentId);

        String name = createJobName("document", projectVersion);
        Pair<List<ArtifactAppEntity>, List<TraceAppEntity>> response =
            appEntityRetrievalService.getEntitiesInDocument(projectVersion,
                document);
        return runLayoutJob(name, response.getValue0(), response.getValue1());
    }

    @PostMapping(AppRoutes.Projects.Layout.saveLayoutForArtifact)
    public void saveArtifactPosition(@RequestBody ArtifactAppEntity artifactAppEntity) {
        //TODO: Plan out database entities (can we re-use existing ones?)
    }

    private JobAppEntity runLayoutJob(String jobName,
                                      List<ArtifactAppEntity> artifacts,
                                      List<TraceAppEntity> traces) throws JobInstanceAlreadyCompleteException,
        JobExecutionAlreadyRunningException, JobParametersInvalidException, JobRestartException {
        JobDbEntity jobDbEntity = jobService.createNewJob(JobType.GENERATE_LAYOUT, jobName);
        CreateLayoutJob layoutGenerator = new CreateLayoutJob(jobDbEntity, serviceProvider, artifacts, traces);

        //TODO: Include our own service provider
        jobService.runJobWorker(jobDbEntity, layoutGenerator.getServiceProvider(), layoutGenerator);

        return JobAppEntity.createFromJob(jobDbEntity);
    }

    private String createJobName(String entityName, ProjectVersion projectVersion) {
        return String.format("Generating layout for %s: %s", entityName, projectVersion.getProject().getName());
    }
}
