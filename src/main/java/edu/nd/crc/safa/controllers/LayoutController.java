package edu.nd.crc.safa.controllers;

import edu.nd.crc.safa.entities.Layout;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.repositories.LayoutRepository;
import edu.nd.crc.safa.repositories.ProjectRepository;
import edu.nd.crc.safa.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.responses.ServerResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LayoutController extends BaseController {

    LayoutRepository layoutRepository;

    @Autowired
    public LayoutController(ProjectRepository projectRepository,
                            ProjectVersionRepository projectVersionRepository,
                            LayoutRepository layoutRepository) {
        super(projectRepository, projectVersionRepository);
        this.layoutRepository = layoutRepository;
    }

    @PostMapping("projects/{projectId}/trees/{treeId}/layout/")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse postTreeLayout(@PathVariable String projectId,
                                         @PathVariable String treeId,
                                         @RequestBody String b64EncodedLayout) throws Exception {
        Project project = getProject(projectId);
        Layout newLayout = new Layout(project, treeId, b64EncodedLayout);
        this.layoutRepository.save(newLayout);
        return new ServerResponse(newLayout);
    }

    @GetMapping(value = "projects/{projectId}/trees/{treeId}/layout/")
    public String getTreeLayout(@PathVariable String projectId,
                                @PathVariable String treeId) throws ServerError {
        Project project = getProject(projectId);
        Layout layout = this.layoutRepository.findByProjectAndTreeId(project, treeId);
        return layout.getData();
    }
}
