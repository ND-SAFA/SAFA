package edu.nd.crc.safa.controllers;

import edu.nd.crc.safa.entities.sql.Project;
import edu.nd.crc.safa.repositories.sql.ProjectRepository;
import edu.nd.crc.safa.repositories.sql.ProjectVersionRepository;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.responses.ServerResponse;
import edu.nd.crc.safa.services.TreeService;
import edu.nd.crc.safa.services.VersionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TreeController extends BaseController {

    TreeService treeService;
    VersionService versionService;

    @Autowired
    public TreeController(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository,
                          TreeService treeService) {
        super(projectRepository, projectVersionRepository);
    }

    @GetMapping("projects/{projectId}/parents/{node}")
    public ServerResponse getParentNodes(@PathVariable String projectId,
                                         @PathVariable String node,
                                         @RequestParam String rootType) throws ServerError {
        return new ServerResponse(treeService.parents(projectId, node, rootType));
    }

    @GetMapping("projects/{projectId}/nodes/")
    public ServerResponse nodes(@PathVariable String projectId,
                                @RequestParam String nodeType) throws ServerError {
        return new ServerResponse(treeService.nodes(projectId, nodeType));
    }

    @GetMapping("projects/{projectId}/nodes/warnings")
    public ServerResponse getNodeWarnings(@PathVariable String projectId) {
        return new ServerResponse(treeService.getNodeWarnings());
    }

    @GetMapping("projects/{projectId}/trees/")
    public ServerResponse trees(@PathVariable String projectId,
                                @RequestParam String rootType) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(treeService.trees(project, rootType));
    }

    @GetMapping("projects/{projectId}/trees/{treeId}/")
    public ServerResponse tree(@PathVariable String projectId,
                               @PathVariable String treeId,
                               @RequestParam String rootType) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(versionService.tree(project, treeId, rootType));
    }
}
