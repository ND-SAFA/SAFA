package edu.nd.crc.safa.features.rules.controllers;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.rules.entities.app.RuleAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.features.rules.entities.db.Rule;
import edu.nd.crc.safa.features.rules.repositories.RuleRepository;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;
import edu.nd.crc.safa.features.rules.parser.ParserRule;
import edu.nd.crc.safa.features.rules.parser.RuleName;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Responsible for creating, retrieving, and deleting warnings
 * in projects.
 */
@RestController
public class RuleController extends BaseController {

    private final RuleRepository ruleRepository;
    private final AppEntityRetrievalService appEntityRetrievalService;

    @Autowired
    public RuleController(ResourceBuilder resourceBuilder,
                          RuleRepository ruleRepository,
                          AppEntityRetrievalService appEntityRetrievalService) {
        super(resourceBuilder);
        this.ruleRepository = ruleRepository;
        this.appEntityRetrievalService = appEntityRetrievalService;
    }

    /**
     * Returns the current warnings in the artifact tree of given project version.
     *
     * @param versionId The ID of the project version whose warnings are retrieved.
     * @return Mapping of artifact id's to the warnings objects present in those artifacts.
     * @throws SafaError Throws error if user does not have read permission on project version.
     */
    @GetMapping(AppRoutes.Projects.Rules.GET_WARNINGS_IN_PROJECT_VERSION)
    public Map<String, List<RuleName>> getWarningsInProjectVersion(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        return this.appEntityRetrievalService.retrieveWarningsInProjectVersion(projectVersion);
    }

    @PostMapping(AppRoutes.Projects.Rules.CREATE_WARNING_IN_PROJECT)
    public RuleAppEntity createWarningInProject(@PathVariable UUID projectId,
                                                @RequestBody RuleAppEntity ruleAppEntity) {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();

        // Step - Parse rule
        ParserRule parserRule = new ParserRule(
            ruleAppEntity.getName(),
            ruleAppEntity.getDescription(),
            ruleAppEntity.toString());
        assert parserRule.isValid();

        // Step - Create and save persistent rule
        Rule rule = new Rule(project, ruleAppEntity);
        ruleRepository.save(rule);
        ruleAppEntity.setId(rule.getId().toString());

        return ruleAppEntity;
    }
}
