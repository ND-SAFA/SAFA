package edu.nd.crc.safa.server.controllers;

import java.util.stream.Collectors;

import edu.nd.crc.safa.config.Neo4J;
import edu.nd.crc.safa.db.entities.app.TestQuery;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.importer.Puller;
import edu.nd.crc.safa.db.repositories.sql.ProjectRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectVersionRepository;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.responses.ServerResponse;
import edu.nd.crc.safa.server.services.VersionService;

import org.neo4j.driver.Result;
import org.neo4j.driver.Session;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VersionController extends BaseController {

    Neo4J neo4J;
    Puller mPuller;
    VersionService versionService;

    @Autowired
    public VersionController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             Neo4J neo4J,
                             Puller mPuller,
                             VersionService versionService) {
        super(projectRepository, projectVersionRepository);
        this.neo4J = neo4J;
        this.mPuller = mPuller;
        this.versionService = versionService;
    }

    @PostMapping("/project/{projectId}/test-query/")
    public ServerResponse testQuery(@PathVariable String projectId,
                                    @RequestBody TestQuery query) throws Exception {
        Session session = neo4J.createSession();
        Result result = session.run(query.getQuery());
        return new ServerResponse(result.stream().collect(Collectors.toList()));
    }

    @GetMapping("projects/{projectId}/versions/")
    public ServerResponse versions(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(versionService.versions(project));
    }

    @GetMapping("projects/{projectId}/trees/{treeId}/versions/{version}")
    public ServerResponse versions(@PathVariable String projectId,
                                   @PathVariable String treeId,
                                   @PathVariable int version,
                                   @RequestParam String rootType) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(versionService.versions(project, treeId, version, rootType));
    }

    @PostMapping("projects/{projectId}/versions/")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public ServerResponse createNewVersionTag(@PathVariable String projectId) {
        return new ServerResponse(versionService.versionsTag(projectId));
    }
}
