package features.memberships.logic;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.features.users.entities.db.ProjectRole;

import common.AbstractSharingTest;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

public class TestMemberRetrieval extends AbstractSharingTest {
    /**
     * Test sharing a project will show new members.
     *
     * @throws Exception If HTTP error occurs.
     */
    @Test
    void newMemberFoundWhenRetrievingMembers() throws Exception {
        // Step - Get projects for user who got shared with
        JSONArray members = retrievalTestService.getProjectMembers(projectVersion.getProject());

        // VP - Verify that shared project is visible
        assertThat(members.length()).isEqualTo(2);

        // Step - Retrieve member JSON
        JSONObject memberJson = members.getJSONObject(1);

        // VP - Verify email of other member
        String otherMemberEmail = memberJson.getString("email");
        assertThat(otherMemberEmail).isEqualTo(Sharee.email);

        // VP - Verify role of other member
        String memberRole = memberJson.getString("role");
        assertThat(memberRole).isEqualTo(getShareePermission().toString());
    }

    @Override
    protected ProjectRole getShareePermission() {
        return ProjectRole.ADMIN;
    }
}
