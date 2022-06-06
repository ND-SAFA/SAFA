package edu.nd.crc.safa.importer.flatfiles;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.EntityVersionService;

import org.json.JSONException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/**
 * Responsible for parsing flat files including reading,
 * validating, and storing their data.
 */
@Component
@Scope("singleton")
public class ArtifactFileParser {

    EntityVersionService entityVersionService;

    @Autowired
    public ArtifactFileParser(EntityVersionService entityVersionService) {
        this.entityVersionService = entityVersionService;
    }

    public EntityCreation<ArtifactAppEntity, String> parseArtifactFiles(ProjectVersion projectVersion,
                                                                        TIMParser TIMParser)
        throws JSONException, SafaError {

        Map<String, ArtifactAppEntity> artifacts = new Hashtable<>();
        List<String> errors = new ArrayList<>();
        for (ArtifactFile artifactDefinitionJson : TIMParser.getArtifactTypeDefinitions()) {
            EntityCreation<ArtifactAppEntity, String> entityCreationResponse =
                artifactDefinitionJson.parseArtifacts(projectVersion);
            for (ArtifactAppEntity artifactAppEntity : entityCreationResponse.getEntities()) {
                if (artifacts.containsKey(artifactAppEntity.name)) {
                    errors.add("Duplicate artifact found:" + artifactAppEntity.name);
                } else {
                    artifacts.put(artifactAppEntity.name, artifactAppEntity);
                }
            }
            errors.addAll(entityCreationResponse.getErrors());
        }
        return new EntityCreation<>(new ArrayList<>(artifacts.values()), errors);
    }
}
