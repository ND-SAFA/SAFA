package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.TraceApproval;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.responses.ServerResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
public class TraceLinkController extends BaseController {

    TraceLinkRepository traceLinkRepository;

    @Autowired
    public TraceLinkController(ProjectRepository projectRepository,
                               ProjectVersionRepository projectVersionRepository,
                               TraceLinkRepository traceLinkRepository) {
        super(projectRepository, projectVersionRepository);
        this.traceLinkRepository = traceLinkRepository;
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

    private ServerResponse changeApprovedHandler(UUID traceLinkId, TraceApproval approvalStatus) throws ServerError {
        Optional<TraceLink> traceLinkQuery = this.traceLinkRepository.findById(traceLinkId);
        if (traceLinkQuery.isPresent()) {
            TraceLink traceLink = traceLinkQuery.get();
            traceLink.setApprovalStatus(approvalStatus);
            this.traceLinkRepository.save(traceLink);
            return new ServerResponse("Trace link was successfully approved");
        } else {
            throw new ServerError("Could not find trace link with id:" + traceLinkId);
        }
    }
}
