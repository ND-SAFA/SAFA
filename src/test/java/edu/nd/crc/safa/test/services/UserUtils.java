package edu.nd.crc.safa.test.services;

import java.util.function.Supplier;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

public class UserUtils {

    public static <T> T asSuperuser(SafaUser asUser, Supplier<T> func) {
        SafaUserService safaUserService = ServiceProvider.getInstance().getSafaUserService();
        boolean superuserState = asUser.isSuperuser();

        safaUserService.addSuperUser(asUser);
        T output = func.get();

        if (!superuserState) {
            safaUserService.removeSuperUser(asUser);
        }

        return output;
    }

    public static void asSuperuser(SafaUser asUser, Runnable func) {
        asSuperuser(asUser, () -> {func.run(); return null;});
    }

    public static <T> T asActiveSuperuser(SafaUser asUser, Supplier<T> func) {
        PermissionService permissionService = ServiceProvider.getInstance().getPermissionService();
        boolean isActive = permissionService.isActiveSuperuser(asUser);

        return asSuperuser(asUser, () -> {
            permissionService.setActiveSuperuser(asUser, true);
            T output = func.get();
            permissionService.setActiveSuperuser(asUser, isActive);
            return output;
        });
    }

    public static void asActiveSuperuser(SafaUser asUser, Runnable func) {
        asActiveSuperuser(asUser, () -> {func.run(); return null;});
    }
}
