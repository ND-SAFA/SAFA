package unit.flatfile;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.entities.database.Artifact;
import edu.nd.crc.safa.entities.database.ArtifactBody;
import edu.nd.crc.safa.entities.database.ArtifactType;
import edu.nd.crc.safa.entities.database.Project;
import edu.nd.crc.safa.entities.database.ProjectVersion;
import edu.nd.crc.safa.entities.database.TraceLink;
import edu.nd.crc.safa.flatfiles.TraceLinkGenerator;
import edu.nd.crc.safa.responses.ServerError;

import org.javatuples.Pair;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

public class TestTraceLinkGenerator extends EntityBaseTest {

    @Autowired
    TraceLinkGenerator traceLinkGenerator;

    @Test
    public void testTraceLinkGeneration() throws ServerError {
        String sourceTypeName = "requirement";
        String targetTypeName = "design";


        ProjectVersion projectVersion = createProjectWithNewVersion("testProject");
        Project project = projectVersion.getProject();
        ArtifactType sourceType = new ArtifactType(project, sourceTypeName);
        this.artifactTypeRepository.save(sourceType);
        ArtifactType targetType = new ArtifactType(project, targetTypeName);
        this.artifactTypeRepository.save(targetType);

        // VP - no error when generating between no artifacts
        Pair<ArtifactType, ArtifactType> artifactTypes = new Pair<>(sourceType, targetType);
        List<TraceLink> newLinks = traceLinkGenerator.generateLinksBetweenTypes(projectVersion, artifactTypes);
        assertThat(newLinks.size()).as("empty links works").isEqualTo(0);


        // VP - able to generate artifacts between similar artifacts
        String sourceOneName = "RE-8";
        String sourceTwoName = "RE-9";
        String targetOneName = "D-8";
        String targetTwoName = "D-9";
        String content = "this is a content type";
        String contentTwo = "no words in common";

        createArtifact(projectVersion, sourceType, sourceOneName, "", content);
        createArtifact(projectVersion, sourceType, sourceTwoName, "", contentTwo);
        createArtifact(projectVersion, targetType, targetOneName, "", content);
        createArtifact(projectVersion, targetType, targetTwoName, "", contentTwo);
        newLinks = traceLinkGenerator.generateLinksBetweenTypes(projectVersion, artifactTypes);
        assertThat(newLinks.size()).as("links found").isEqualTo(2);

        TraceLink linkOne = getLinkWithSourceName(newLinks, sourceOneName);
        assertThat(linkOne.getTargetName()).as("link source name").isEqualTo(targetOneName);

        TraceLink linkTwo = getLinkWithSourceName(newLinks, sourceTwoName);
        assertThat(linkTwo.getTargetName()).as("link source name").isEqualTo(targetTwoName);

        //cleanup
        projectService.deleteProject(project);
    }

    private TraceLink getLinkWithSourceName(List<TraceLink> links, String sourceName) {
        for (TraceLink link : links) {
            if (link.getSourceName().equals(sourceName)) {
                return link;
            }
        }
        throw new RuntimeException("Could not find link with source name:" + sourceName);
    }

    private void createArtifact(ProjectVersion projectVersion,
                                ArtifactType artifactType,
                                String name,
                                String summary,
                                String content) {
        Project project = projectVersion.getProject();
        Artifact artifact = new Artifact(project, artifactType, name);
        this.artifactRepository.save(artifact);

        ArtifactBody artifactBody = new ArtifactBody(projectVersion, artifact, summary, content);
        this.artifactBodyRepository.save(artifactBody);
    }
}
