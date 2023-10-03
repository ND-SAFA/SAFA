package edu.nd.crc.safa.features.flatfiles.builder;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.Data;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

@Data
public class FlatFileBuilderArgs {
    private final SafaUser user;
    private final List<MultipartFile> files;
    private final ProjectVersion projectVersion;
    private final boolean asCompleteSet;
    private final ProjectCommitDefinition projectCommitDefinition;
    private TimFileParser timFileParser;
    private FlatFileParser flatFileParser;
    private List<ArtifactAppEntity> artifactsAdded;
    private JSONObject timFileJson;

    public FlatFileBuilderArgs(SafaUser user,
                               List<MultipartFile> files,
                               ProjectVersion projectVersion,
                               boolean asCompleteSet,
                               boolean failOnError) {
        this.user = user;
        this.files = files;
        this.projectVersion = projectVersion;
        this.asCompleteSet = asCompleteSet;
        this.projectCommitDefinition = new ProjectCommitDefinition(projectVersion, failOnError);
    }
}
