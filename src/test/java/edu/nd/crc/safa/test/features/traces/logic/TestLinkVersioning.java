package edu.nd.crc.safa.test.features.traces.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.AbstractVersionedEntityTest;
import edu.nd.crc.safa.test.requests.FlatFileRequest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

public class TestLinkVersioning extends AbstractVersionedEntityTest<TraceAppEntity, TraceLinkVersion> {
    static String FLAT_FILES_PATH = ProjectPaths.Resources.Tests.MINI;
    static double ORIGINAL_SCORE = 1;
    static double MODIFIED_SCORE = 3.14;
    static String ORIGINAL_EXPLANATION = "initial explanation";
    static String MODIFIED_EXPLANATION = "new explanation";

    @Override
    protected void loadDataIntoProjectVersion(ProjectVersion projectVersion) throws Exception {
        FlatFileRequest.updateProjectVersionFromFlatFiles(projectVersion, FLAT_FILES_PATH);
    }

    @Override
    protected List<TraceLinkVersion> getAllVersions(Project project) {
        return traceLinkVersionRepository.getProjectLinks(project);
    }

    @Override
    protected Optional<TraceLinkVersion> getEntityVersionByProjectVersion(TraceLinkVersion entity,
                                                                          ProjectVersion projectVersion) {

        return traceLinkVersionRepository.findByProjectVersionAndTraceLink(projectVersion, entity.getTraceLink());
    }

    @Override
    protected void modifyEntityInCommit(CommitBuilder commitBuilder, TraceLinkVersion entity) {
        entity.setScore(MODIFIED_SCORE);
        entity.setExplanation(MODIFIED_EXPLANATION);
        TraceAppEntity linkAppEntity = this.traceLinkVersionRepository.retrieveAppEntityFromVersionEntity(entity);
        commitBuilder.withModifiedTrace(linkAppEntity);
    }

    @Override
    protected void removeEntityInCommit(CommitBuilder commitBuilder, TraceLinkVersion entity) {
        TraceAppEntity linkAppEntity = this.traceLinkVersionRepository.retrieveAppEntityFromVersionEntity(entity);
        commitBuilder.withRemovedTrace(linkAppEntity);
    }

    @Override
    protected void verifyChangeToEntity(TraceLinkVersion entity) {
        assertThat(entity.getScore()).isEqualTo(MODIFIED_SCORE);
        assertThat(entity.getExplanation()).isEqualTo(MODIFIED_EXPLANATION);
    }

    @Override
    protected void verifyNoChangeToEntity(TraceLinkVersion entity) {
        assertThat(entity.getScore()).isEqualTo(ORIGINAL_SCORE);
        assertThat(entity.getExplanation()).isEqualTo(ORIGINAL_EXPLANATION);
    }
}
