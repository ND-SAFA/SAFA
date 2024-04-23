package edu.nd.crc.safa.test.services.requests;

import java.util.List;
import java.util.function.Consumer;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.controllers.ProjectController;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.AndBuilder;
import edu.nd.crc.safa.test.services.builders.BuilderState;
import edu.nd.crc.safa.test.services.builders.CustomAttributeBuilder;

import com.fasterxml.jackson.core.type.TypeReference;
import lombok.AllArgsConstructor;
import org.json.JSONObject;
import org.springframework.test.web.servlet.ResultMatcher;

@AllArgsConstructor
public class CommonProjectRequests {
    private BuilderState state;

    public static List<JobAppEntity> getUserJobs() throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Jobs.Meta.GET_USER_JOBS)
            .getAsArray(JobAppEntity.class);
    }

    public static List<JobAppEntity> getProjectJobs(edu.nd.crc.safa.features.projects.entities.db.Project project) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Jobs.Meta.GET_PROJECT_JOBS)
            .withProject(project)
            .getAsArray(JobAppEntity.class);
    }

    public static List<TraceAppEntity> getGeneratedLinks(ProjectVersion projectVersion) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Links.GET_GENERATED_LINKS_IN_PROJECT_VERSION)
            .withVersion(projectVersion)
            .getAsArray(TraceAppEntity.class);
    }

    public static JSONObject shareProject(Project project,
                                          String email,
                                          ProjectRole role) {
        MembershipAppEntity membershipAppEntity = new MembershipAppEntity(email, role.toString());
        return SafaRequest
            .withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(project.getProjectId())
            .postWithJsonObject(membershipAppEntity);
    }

    public static JSONObject shareProject(Project project,
                                          String email,
                                          ProjectRole role,
                                          ResultMatcher resultMatcher) {
        MembershipAppEntity request = new MembershipAppEntity(email, role.name());
        return SafaRequest
            .withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(project.getProjectId())
            .postWithJsonObject(request, resultMatcher);
    }

    public static ProjectIdAppEntity transferProjectOwnership(Project project,
                                                              ProjectController.TransferOwnershipDTO transferDetails) {
        return SafaRequest.withRoute(AppRoutes.Projects.TRANSFER_OWNERSHIP)
            .withProject(project)
            .putAndParseResponse(transferDetails, new TypeReference<>(){});
    }

    public static JSONObject transferProjectOwnership(Project project,
                                                      ProjectController.TransferOwnershipDTO transferDetails,
                                                      ResultMatcher resultMatcher) {
        return SafaRequest.withRoute(AppRoutes.Projects.TRANSFER_OWNERSHIP)
            .withProject(project)
            .putWithJsonObject(transferDetails, resultMatcher);
    }

    public AndBuilder<CommonProjectRequests, CustomAttributeAppEntity> createCustomAttribute(String projectParam,
                                                                                             Consumer<CustomAttributeBuilder> consumer) {
        Project project = state.getProject(projectParam);
        CustomAttributeBuilder builder = new CustomAttributeBuilder();
        consumer.accept(builder);
        CustomAttribute customAttribute = builder.getCustomAttribute();
        CustomAttributeAppEntity customAttributeAppEntity = new CustomAttributeAppEntity(customAttribute);
        CustomAttributeAppEntity createAttribute = SafaRequest
            .withRoute(AppRoutes.Attribute.ROOT)
            .withProject(project)
            .postWithJsonObject(customAttributeAppEntity, CustomAttributeAppEntity.class);
        return new AndBuilder<>(this, createAttribute, this.state);
    }
}
