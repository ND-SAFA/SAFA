package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.services.RevisionNotificationService;
import edu.nd.crc.safa.server.services.TraceLinkService;
import edu.nd.crc.safa.server.services.VersionService;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
public class TraceLinkController extends BaseController {

    TraceLinkRepository traceLinkRepository;
    TraceLinkService traceLinkService;
    VersionService versionService;
    RevisionNotificationService revisionNotificationService;

    @Autowired
    public TraceLinkController(ProjectRepository projectRepository,
                               ProjectVersionRepository projectVersionRepository,
                               TraceLinkRepository traceLinkRepository,
                               TraceLinkService traceLinkService,
                               VersionService versionService,
                               RevisionNotificationService revisionNotificationService) {
        super(projectRepository, projectVersionRepository);
        this.traceLinkRepository = traceLinkRepository;
        this.traceLinkService = traceLinkService;
        this.versionService = versionService;
        this.revisionNotificationService = revisionNotificationService;
    }

    @GetMapping("/projects/{projectId}/links/generated")
    public ServerResponse getGeneratedLinks(@PathVariable UUID projectId) {
        Project project = this.projectRepository.findByProjectId(projectId);
        List<TraceLink> projectLinks = this.traceLinkRepository.getGeneratedLinks(project);
        return new ServerResponse(TraceApplicationEntity.createEntities(projectLinks));
    }

    @PutMapping("/projects/links/{traceLinkId}/approve")
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse approveTraceLink(@PathVariable UUID traceLinkId) throws ServerError {
        return changeApprovedHandler(traceLinkId, TraceApproval.APPROVED);
    }

    @PutMapping("/projects/links/{traceLinkId}/decline")
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse declineTraceLink(@PathVariable UUID traceLinkId) throws ServerError {
        return changeApprovedHandler(traceLinkId, TraceApproval.DECLINED);
    }

    @PostMapping("/projects/versions/{versionId}/links/create/{sourceName}/{targetName}")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewTraceLInk(@PathVariable UUID versionId,
                                             @PathVariable String sourceName,
                                             @PathVariable String targetName) throws ServerError {
        ProjectVersion projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        Pair<TraceLink, ParserError> creationResponse = this.traceLinkService.createTrace(projectVersion, sourceName,
            targetName);
        if (creationResponse.getValue0() == null) {
            return new ServerResponse(creationResponse.getValue1());
        }
        TraceLink traceLink = creationResponse.getValue0();
        this.traceLinkRepository.saveAll(List.of(traceLink));
        this.revisionNotificationService.broadcastTrace(projectVersion.getProject(),
            new TraceApplicationEntity(traceLink));
        return new ServerResponse(new TraceApplicationEntity(traceLink));
    }

    private ServerResponse changeApprovedHandler(UUID traceLinkId, TraceApproval approvalStatus) throws ServerError {
        Optional<TraceLink> traceLinkQuery = this.traceLinkRepository.findById(traceLinkId);
        if (traceLinkQuery.isPresent()) {
            TraceLink traceLink = traceLinkQuery.get();
            traceLink.setApprovalStatus(approvalStatus);
            this.traceLinkRepository.save(traceLink);
            Project project = traceLink.getSourceArtifact().getProject();
            this.revisionNotificationService.broadcastTrace(project, new TraceApplicationEntity(traceLink));
            return new ServerResponse("Trace link was successfully approved");
        } else {
            throw new ServerError("Could not find trace link with id:" + traceLinkId);
        }
    }
}
