package edu.nd.crc.safa.features.github.entities.api;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.graphql.entities.DefaultPaginatable;
import edu.nd.crc.safa.utilities.graphql.entities.Edges;
import edu.nd.crc.safa.utilities.graphql.entities.GraphQlResponse;
import edu.nd.crc.safa.utilities.graphql.entities.Paginatable;

import lombok.Data;
import lombok.Getter;
import lombok.ToString;

/**
 * Response for {@code github/GetRepositories.graphql}.
 */
@Getter
@ToString(callSuper = true)
public class GithubGraphQlRepositoriesResponse extends GraphQlResponse<GithubGraphQlRepositoriesResponse.Payload> {

    @Data
    public static class Payload implements DefaultPaginatable {

        private Viewer viewer;

        @Data
        public static class Viewer implements Paginatable {
            private Edges<Repository> repositories;

            @Override
            public void paginate(SafaUser user) {
                ServiceProvider.getInstance().getGithubGraphQlService().paginateRepositories(user, repositories);
                repositories.getEdges().forEach(edge -> edge.paginate(user));
            }
        }
    }
}
