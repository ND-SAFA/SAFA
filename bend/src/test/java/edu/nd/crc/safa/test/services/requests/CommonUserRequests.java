package edu.nd.crc.safa.test.services.requests;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.BuilderState;

import lombok.AllArgsConstructor;
import org.json.JSONObject;

@AllArgsConstructor
public class CommonUserRequests {
    private BuilderState state;

    public CommonUserRequests makeUserSuperuser(SafaUser user) {
        state.getServiceProvider().getSafaUserService().addSuperUser(user);
        return this;
    }

    public CommonUserRequests activateSuperuser() {
        try {
            SafaRequest.withRoute(AppRoutes.Accounts.SuperUser.ACTIVATE)
                .putWithJsonObject(new JSONObject());
        } catch (Exception e) {
            throw new AssertionError(e);
        }
        return this;
    }

    public CommonUserRequests deactivateSuperuser() {
        try {
            SafaRequest.withRoute(AppRoutes.Accounts.SuperUser.DEACTIVATE)
                .putWithJsonObject(new JSONObject());
        } catch (Exception e) {
            throw new AssertionError(e);
        }
        return this;
    }
}
