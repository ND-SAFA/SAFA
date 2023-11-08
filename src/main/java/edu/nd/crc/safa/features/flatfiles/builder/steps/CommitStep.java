package edu.nd.crc.safa.features.flatfiles.builder.steps;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderArgs;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.ProjectChanger;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class CommitStep implements IFlatFileBuilderStep {
    @Override
    public void perform(FlatFileBuilderArgs state, ServiceProvider serviceProvider) throws Exception {
        ProjectCommitDefinition projectCommitDefinition = state.getProjectCommitDefinition();
        ProjectVersion projectVersion = state.getProjectVersion();
        SafaUser user = state.getUser();
        boolean asCompleteSet = state.isAsCompleteSet();

        // Step - Commit all project entities
        ProjectEntities projectEntities = new ProjectEntities(
            projectCommitDefinition.getArtifacts().getAdded(),
            projectCommitDefinition.getTraces().getAdded()
        );
        ProjectChanger projectChanger = new ProjectChanger(projectVersion, serviceProvider);
        if (asCompleteSet) {
            projectChanger.setEntitiesAsCompleteSet(projectEntities, user);
        } else {
            projectChanger.commit(user, projectCommitDefinition);
        }
        serviceProvider.getCommitErrorRepository().saveAll(projectCommitDefinition.getErrors());
    }
}
