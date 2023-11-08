package edu.nd.crc.safa.test.services.builders;

import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Function;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class DatabaseTestBuilder {
    private final ServiceProvider serviceProvider;
    private final BuilderState state;

    public DatabaseTestBuilder(ServiceProvider serviceProvider, BuilderState builderState) {
        this.serviceProvider = serviceProvider;
        this.state = builderState;
    }

    public <T> AndBuilder<DatabaseTestBuilder, T> version(BiFunction<BuilderState, VersionTestBuilder, T> consumer) {
        VersionTestBuilder versionTestBuilder = new VersionTestBuilder(this.serviceProvider);
        T result = consumer.apply(this.state, versionTestBuilder);
        return new AndBuilder<>(this, result, this.state);
    }

    public AndBuilder<DatabaseTestBuilder, ProjectVersion> version(Function<VersionTestBuilder, ProjectVersion> consumer) {
        return version((s, v) -> consumer.apply(v));
    }

    public AndBuilder<DatabaseTestBuilder, Project> project(SafaUser user, Consumer<PBuilder> consumer) {
        PBuilder projectBuilder = new PBuilder();
        consumer.accept(projectBuilder);
        Project project = projectBuilder.getProject();
        project = serviceProvider
            .getProjectService()
            .createProject(project.getName(), project.getDescription(), user);
        return new AndBuilder<>(this, project, this.state);
    }

    public AndBuilder<DatabaseTestBuilder, Project> project(SafaUser user) {
        return project(user, PBuilder::defaultValues);
    }

    public DatabaseTestBuilder withType(Project project, Consumer<TypeBuilder> consumer) {
        TypeBuilder typeBuilder = new TypeBuilder();
        consumer.accept(typeBuilder);
        ArtifactType artifactType = typeBuilder.getArtifactType();
        artifactType.setProject(project);
        this.serviceProvider.getTypeService().saveArtifactType(artifactType);
        return this;
    }
}
