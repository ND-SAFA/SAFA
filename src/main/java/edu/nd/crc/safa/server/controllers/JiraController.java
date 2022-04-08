package edu.nd.crc.safa.server.controllers;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.JIRAProjectPullRequest;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

/**
 * Responsible for pulling and syncing JIRA projects with Safa projects.
 */
@Controller
public class JiraController extends BaseController {

    AppEntityRetrievalService appEntityRetrievalService;
    ProjectService projectService;

    @Autowired
    public JiraController(ResourceBuilder resourceBuilder,
                          AppEntityRetrievalService appEntityRetrievalService,
                          ProjectService projectService) {
        super(resourceBuilder);
        this.appEntityRetrievalService = appEntityRetrievalService;
        this.projectService = projectService;
    }

    @PostMapping(AppRoutes.Projects.Import.pullJiraProject)
    public ProjectEntities pullJiraProject(@RequestBody JIRAProjectPullRequest jiraProjectPullRequest) {
        Project project = new Project();
        project.setName("DUMMY NAME");
        project.setDescription("DUMMY DESCRIPTION");
        this.projectService.saveProjectWithCurrentUserAsOwner(project);
        ProjectVersion projectVersion = this.projectService.createBaseProjectVersion(project);
        return appEntityRetrievalService.retrieveProjectEntitiesAtProjectVersion(projectVersion);
    }
}
