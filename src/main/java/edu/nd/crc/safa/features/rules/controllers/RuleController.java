package edu.nd.crc.safa.features.rules.controllers;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.entities.app.RuleAppEntity;
import edu.nd.crc.safa.features.rules.entities.db.Rule;
import edu.nd.crc.safa.features.rules.parser.ParserRule;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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

    @Autowired
    public RuleController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Returns the current warnings in the artifact tree of given project version.
     *
     * @param versionId The ID of the project version whose warnings are retrieved.
     * @return Mapping of artifact id's to the warnings objects present in those artifacts.
     * @throws SafaError Throws error if user does not have read permission on project version.
     */
    @GetMapping(AppRoutes.Rules.GET_WARNINGS_IN_PROJECT_VERSION)
    public Map<UUID, List<RuleName>> getWarningsInProjectVersion(@PathVariable UUID versionId) throws SafaError {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
                .withPermission(ProjectPermission.VIEW, user).get();
        return getServiceProvider().getWarningService().retrieveWarningsInProjectVersion(projectVersion);
    }

    @PostMapping(AppRoutes.Rules.CREATE_WARNING_IN_PROJECT)
    public RuleAppEntity createWarningInProject(@PathVariable UUID projectId,
                                                @RequestBody RuleAppEntity ruleAppEntity) {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        Project project = getResourceBuilder().fetchProject(projectId)
                .withPermission(ProjectPermission.EDIT, user).get();

        // Step - Parse rule
        ParserRule parserRule = new ParserRule(
            ruleAppEntity.getName(),
            ruleAppEntity.getDescription(),
            ruleAppEntity.toString());
        assert parserRule.isValid();

        // Step - Create and save persistent rule
        Rule rule = new Rule(project, ruleAppEntity);
        getServiceProvider().getRuleRepository().save(rule);
        ruleAppEntity.setId(rule.getId().toString());

        return ruleAppEntity;
    }
}
