package unit.neo4j;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.Optional;

import edu.nd.crc.safa.db.entities.neo4j.ArtifactNode;

import org.junit.jupiter.api.Test;

public class ArtifactNodeOperations extends BaseNeo {


    @Test
    public void createArtifact() {
        ArtifactNode node = new ArtifactNode("RE-8", "requirement", "this is a body");
        this.artifactNodeRepository.save(node);

        Optional<ArtifactNode> nodeQuery = this.artifactNodeRepository.findById("RE-8");
        assertThat(nodeQuery.isPresent()).isTrue();
        ArtifactNode nodeFound = nodeQuery.get();
        assertThat(nodeFound.getId()).isEqualTo("RE-8");
    }
}
