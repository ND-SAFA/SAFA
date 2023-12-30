package edu.nd.crc.safa.features.permissions.checks;

import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.billing.services.CreditBalanceService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;

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

        CreditBalanceService creditBalanceService = context.getServiceProvider().getCreditBalanceService();
        BillingInfo billingInfo = creditBalanceService.getBillingInfoForOrg(org);
        return billingInfo.getBalance() > minimumBalance;
    }
}
