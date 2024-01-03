package edu.nd.crc.safa.features.permissions.checks.billing;

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

    private final int minimumBalance;

    public MinimumBalanceCheck(int minimumBalance) {
        this.minimumBalance = minimumBalance;
    }

    @Override
    public boolean doCheck(PermissionCheckContext context) {
        Organization org = context.getOrganization();

        if (org == null) {
            return false;
        }

        BillingService billingService = context.getServiceProvider().getBillingService();
        BillingInfo billingInfo = billingService.getBillingInfoForOrg(org);
        return billingInfo.getBalance() > minimumBalance;
    }
}
