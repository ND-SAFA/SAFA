package features.traces.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.CommitBuilder;
import common.AbstractVersionedEntityTest;
import requests.FlatFileRequest;

public class TestLinkVersioning extends AbstractVersionedEntityTest<TraceAppEntity, TraceLinkVersion> {
    static String FLAT_FILES_PATH = ProjectPaths.Resources.Tests.MINI;
    static double ORIGINAL_SCORE = 1;
    static double MODIFIED_SCORE = 3.14;

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
    }

    @Override
    protected void verifyNoChangeToEntity(TraceLinkVersion entity) {
        assertThat(entity.getScore()).isEqualTo(ORIGINAL_SCORE);
    }
}
