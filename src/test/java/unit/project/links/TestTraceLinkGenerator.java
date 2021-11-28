package unit.project.links;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.importer.tracegenerator.TraceLinkGenerator;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;

import org.javatuples.Pair;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Tests that the system is able to generate trace links between two sets of artifacts.
 */
public class TestTraceLinkGenerator extends ApplicationBaseTest {

    @Autowired
    TraceLinkGenerator traceLinkGenerator;

    @Test
    public void testTraceLinkGeneration() {
        String sourceTypeName = "requirement";
        String targetTypeName = "design";
        String projectName = "test-project";

        String sourceOneName = "RE-8";
        String sourceTwoName = "RE-9";
        String targetOneName = "D-8";
        String targetTwoName = "D-9";
        String content = "this is a content type";
        String contentTwo = "no words in common";

        // Step - Create project with source and target types
        dbEntityBuilder.newProject(user, projectName);
        ProjectVersion projectVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        ArtifactType sourceType = dbEntityBuilder.newTypeAndReturn(projectName, sourceTypeName);
        ArtifactType targetType = dbEntityBuilder.newTypeAndReturn(projectName, targetTypeName);

        // VP - no error when generating between no artifacts
        Pair<ArtifactType, ArtifactType> artifactTypes = new Pair<>(sourceType, targetType);
        List<TraceLink> newLinks = traceLinkGenerator.generateLinksBetweenTypes(projectVersion, artifactTypes);
        assertThat(newLinks.size()).as("empty links works").isEqualTo(0);

        // VP - able to generate artifacts between similar artifacts
        dbEntityBuilder
            .newArtifactAndBody(projectName, sourceTypeName, sourceOneName, "", content)
            .newArtifactAndBody(projectName, sourceTypeName, sourceTwoName, "", contentTwo)
            .newArtifactAndBody(projectName, targetTypeName, targetOneName, "", content)
            .newArtifactAndBody(projectName, targetTypeName, targetTwoName, "", contentTwo);

        newLinks = traceLinkGenerator.generateLinksBetweenTypes(projectVersion, artifactTypes);
        assertThat(newLinks.size()).as("links found").isEqualTo(2);

        TraceLink linkOne = getLinkWithSourceName(newLinks, sourceOneName);
        assertThat(linkOne.getTargetName()).as("link source name").isEqualTo(targetOneName);

        TraceLink linkTwo = getLinkWithSourceName(newLinks, sourceTwoName);
        assertThat(linkTwo.getTargetName()).as("link source name").isEqualTo(targetTwoName);
    }

    private TraceLink getLinkWithSourceName(List<TraceLink> links, String sourceName) {
        for (TraceLink link : links) {
            if (link.getSourceName().equals(sourceName)) {
                return link;
            }
        }
        throw new RuntimeException("Could not find link with source name:" + sourceName);
    }
}
