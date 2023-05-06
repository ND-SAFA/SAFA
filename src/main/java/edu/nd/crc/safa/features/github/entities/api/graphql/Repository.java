package edu.nd.crc.safa.features.github.entities.api.graphql;

import java.util.Date;
import java.util.List;
import java.util.function.Consumer;

import edu.nd.crc.safa.utilities.graphql.entities.Edges;
import edu.nd.crc.safa.utilities.graphql.entities.Paginatable;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import org.apache.commons.lang3.NotImplementedException;

@Data
public class Repository implements Paginatable<Repository> {
    private String id;
    private String name;
    private Owner owner;
    @JsonProperty("isPrivate")
    private boolean isPrivate;
    private String url;
    private String description;
    private RepositoryVisibility visibility;
    private Date createdAt;
    private Language primaryLanguage;
    private Branch defaultBranchRef;
    private Edges<Branch> refs;

    @Override
    public Consumer<List<Repository>> getPaginationFunction() {
        throw new NotImplementedException("Not implemented yet.");
    }

}
