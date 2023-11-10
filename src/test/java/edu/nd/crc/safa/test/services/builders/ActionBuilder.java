package edu.nd.crc.safa.test.services.builders;

import static edu.nd.crc.safa.test.common.ApplicationBaseTest.getTokenName;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.features.notifications.documentartifact.IDocumentArtifactTest;
import edu.nd.crc.safa.test.services.CommitTestService;

public class ActionBuilder {
    private final RootBuilder rootBuilder;

    public ActionBuilder(RootBuilder rootBuilder) {
        this.rootBuilder = rootBuilder;
    }

    public ActionBuilder verifyActiveMembers(IUser user, List<String> expectedUsers) {
        String property = String.format("%s-active-members-message-%s", user.getEmail(), UUID.randomUUID());
        return verifyActiveMembers(user, property, expectedUsers);
    }

    public ActionBuilder verifyActiveMembers(IUser user, String property, List<String> expectedUsers) {
        this.rootBuilder
            .notifications(n -> n.getEntityMessage(user)).save(property)
            .and()
            .verify((s, v) -> v.notifications(n -> n.
                verifyMemberNotification(s.getMessage(property), expectedUsers)));
        return this;
    }

    public ActionBuilder createNewUser(String userName, String password, ApplicationBaseTest test) {
        return createNewUser(userName, password, true, test);
    }

    public ActionBuilder createNewUser(String userName, String password, boolean setToken, ApplicationBaseTest test) {
        String token = rootBuilder
            .authorize(a -> a
                .createUser(userName, password)
                .save(userName)
                .and()
                .loginUser(userName, password, setToken, test)
                .get())
            .get();
        if (setToken) {
            this.rootBuilder.store(s -> s.save(getTokenName(userName), token));
        }
        this.rootBuilder.notifications((s, n) -> n.initializeUser(s.getIUser(userName), token));
        return this;
    }

    public ProjectVersion createProjectWithVersion(SafaUser user) {
        return rootBuilder
            .build(b -> b.project(user, PBuilder::defaultValues).save("project"))
            .and()
            .build((s, b) -> b
                .version(v -> v.newVersion(s.getProject("project"))).save("version").get()).get();
    }

    public ActionBuilder createArtifactAndVerifyMessage(ProjectVersion projectVersion,
                                                        IDocumentArtifactTest test) {
        // Step - Create artifact
        ArtifactAppEntity artifact = test.getArtifact();
        ArtifactAppEntity artifactAdded = this.rootBuilder.actions(a -> a.commit(
                CommitBuilder
                    .withVersion(projectVersion)
                    .withAddedArtifact(artifact)
            ).getArtifact(ModificationType.ADDED, 0))
            .get();

        // VP - Verify commit message
        // TODO https://www.notion.so/nd-safa/BE-Tests-Occasionally-Fail-9500d5c1f1d84a76acf429ee3653bb86
        /*
        List<EntityChangeMessage> commitMessages = this.rootBuilder
            .notifications(n -> n
                .getMessages(test.getSharee()))
            .get();

        this.rootBuilder
            .verify(v -> v
                .notifications(n -> n
                    .verifyArtifactTypeMessage(commitMessages.get(1), artifact.getType())
                    .verifySingleEntityChanges(commitMessages.get(2),
                        List.of(NotificationEntity.ARTIFACTS, NotificationEntity.WARNINGS), List.of(1, 0))));
         */

        // Step - Set current artifact with created id
        test.setArtifact(artifactAdded);
        return this;
    }

    public ProjectCommitDefinition commit(CommitBuilder commitBuilder) {
        return CommitTestService.commit(commitBuilder);
    }
}
