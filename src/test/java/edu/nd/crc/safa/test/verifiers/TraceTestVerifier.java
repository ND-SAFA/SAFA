package edu.nd.crc.safa.test.verifiers;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkRepository;

public class TraceTestVerifier {
    public static void assertTraceExists(TraceLinkRepository traceLinkRepository, Project project, String sourceName,
                                         String targetName) {
        assertTraceStatus(traceLinkRepository, project, sourceName, targetName, true);
    }

    public static void assertTraceDoesNotExist(TraceLinkRepository traceLinkRepository, Project project,
                                               String sourceName, String targetName) {
        assertTraceStatus(traceLinkRepository, project, sourceName, targetName, false);
    }

    public static void assertTraceStatus(TraceLinkRepository traceLinkRepository, Project project, String sourceName,
                                         String targetName,
                                         boolean exists) {
        Optional<TraceLink> traceLinkQuery =
            traceLinkRepository.getByProjectAndSourceAndTarget(project,
                sourceName,
                targetName);
        assertThat(traceLinkQuery.isPresent()).isEqualTo(exists);
    }
}
