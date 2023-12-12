package edu.nd.crc.safa.features.flatfiles.builder.steps;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.ProjectChanger;

public class CommitStep implements IFlatFileBuilderStep {
    /**
     * Saves entities in commit to database.
     *
     * @param serviceProvider         Provides access to the database services.
     * @param projectCommitDefinition The commit containing entity modifications.
     * @param asCompleteSet           Whether commit represents the complete set of project entities.
     */
    public static void performCommit(ServiceProvider serviceProvider,
                                     ProjectCommitDefinition projectCommitDefinition,
                                     boolean asCompleteSet) {
        SafaUser user = projectCommitDefinition.getUser();
        // Step - Commit all project entities
        ProjectEntities projectEntities = new ProjectEntities(
            projectCommitDefinition.getArtifacts().getAdded(),
            projectCommitDefinition.getTraces().getAdded()
        );
        ProjectChanger projectChanger = new ProjectChanger(projectCommitDefinition.getCommitVersion(), serviceProvider);
        if (asCompleteSet) {
            projectChanger.setEntitiesAsCompleteSet(projectEntities, user);
        } else {
            projectChanger.commit(user, projectCommitDefinition);
        }
        serviceProvider.getCommitErrorRepository().saveAll(projectCommitDefinition.getErrors());
    }

    /**
     * Saves entities defined in commit to database.
     *
     * @param state           The state of the flat file project builder.
     * @param serviceProvider Provide access to database services.
     * @throws Exception If error occurs while saving or accessing entities.
     */
    @Override
    public void perform(FlatFileBuilderStore state, ServiceProvider serviceProvider) throws Exception {
        performCommit(serviceProvider,
            state.getProjectCommitDefinition(),
            state.isAsCompleteSet());
    }
}
