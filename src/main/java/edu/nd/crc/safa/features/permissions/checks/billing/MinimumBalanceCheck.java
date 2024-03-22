package edu.nd.crc.safa.features.permissions.checks.billing;

import java.util.function.Function;

import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

/**
 * Checks that the credit balance of an organization is greater than some
 * minimum value. If you want to check if an organization can afford a
 * charge, taking into account the payment tier, use {@link CanAffordChargeCheck}.
 */
public class MinimumBalanceCheck implements AdditionalPermissionCheck {

    private final Function<PermissionCheckContext, Integer> minimumBalanceSupplier;
    private Integer cachedMinimumBalance;

    public MinimumBalanceCheck(int minimumBalance) {
        this(context -> minimumBalance);
    }

    public MinimumBalanceCheck(Function<PermissionCheckContext, Integer> minimumBalanceSupplier) {
        this.minimumBalanceSupplier = minimumBalanceSupplier;
    }

    @Override
    public boolean doCheck(PermissionCheckContext context) {
        Organization org = context.getOrganization();

        if (org == null) {
            return false;
        }

        BillingService billingService = context.getServiceProvider().getBillingService();
        BillingInfo billingInfo = billingService.getBillingInfoForOrg(org);
        return billingInfo.getBalance() >= getMinimumBalance(context);
    }

    @Override
    public String getMessage() {
        return "Organization credit balance must be at least: " + getMinimumBalance(null);
    }

    @Override
    public boolean superuserCanOverride() {
        return true;
    }

    private int getMinimumBalance(PermissionCheckContext context) {
        if (cachedMinimumBalance == null) {
            if (context == null) {
                cachedMinimumBalance = -1;
            } else {
                cachedMinimumBalance = minimumBalanceSupplier.apply(context);
            }
        }
        return cachedMinimumBalance;
    }
}
