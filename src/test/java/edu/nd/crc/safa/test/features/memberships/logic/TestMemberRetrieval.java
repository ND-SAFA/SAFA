package edu.nd.crc.safa.test.features.memberships.logic;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.test.common.AbstractSharingTest;

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
        JSONArray members = retrievalService.getProjectMembers(projectVersion.getProject());

        // VP - Verify that shared project is visible
        assertThat(members.length()).isEqualTo(1);

        // Step - Retrieve member JSON
        JSONObject memberJson = null;
        for (int i = 0; i < members.length(); ++i) {
            JSONObject object = members.getJSONObject(i);
            if (object.has("email") && object.getString("email").equals(Sharee.email)) {
                memberJson = object;
            }
        }

        // VP - Verify email of other member
        assertThat(memberJson).isNotNull();

        // VP - Verify role of other member
        String memberRole = memberJson.getString("role");
        assertThat(memberRole).isEqualTo(getShareePermission().toString());
    }

    @Override
    protected ProjectRole getShareePermission() {
        return ProjectRole.ADMIN;
    }
}
