package edu.nd.crc.safa.features.github.entities.api.graphql;

import java.util.Date;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.graphql.entities.Edges;
import edu.nd.crc.safa.utilities.graphql.entities.Paginatable;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class Repository implements Paginatable {
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
    public void paginate(SafaUser user) {
        if (refs != null) {
            ServiceProvider.getInstance()
                .getGithubGraphQlService().paginateBranches(user, refs, name, owner.getLogin());
        }
    }
}
