package edu.nd.crc.safa.features.billing.controllers;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.billing.entities.app.TransactionAppEntity;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;

@Controller
public class BillingController extends BaseController {

    private final BillingService billingService;
    private final PermissionService permissionService;

    public BillingController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                             BillingService billingService, PermissionService permissionService) {
        super(resourceBuilder, serviceProvider);
        this.billingService = billingService;
        this.permissionService = permissionService;
    }

    @PostMapping(AppRoutes.Billing.CHECKOUT)
    public TransactionAppEntity purchaseCredits(@RequestBody PurchaseDetailsDTO purchaseDetails) {
        Organization organization = getResourceBuilder().fetchOrganization(purchaseDetails.getOrganizationId())
            .withPermission(OrganizationPermission.VIEW_BILLING, getCurrentUser())
            .get();
        return billingService.startTransaction(organization, purchaseDetails.getAmount(),
            purchaseDetails.getDescription());
    }

    /**
     * Update an organization's payment tier. Requires the user to be an active superuser
     *
     * @param body The details about which org to update and to what tier
     * @return An empty object (helps with the front end to not return nothing)
     */
    @PutMapping(AppRoutes.Billing.CHANGE_TIER)
    public String updatePaymentTier(@RequestBody ChangePaymentTierDTO body) {
        SafaUser user = getCurrentUser();
        permissionService.requireActiveSuperuser(user);

        Organization organization = getResourceBuilder().fetchOrganization(body.getOrganizationId()).get();
        billingService.updatePaymentTier(organization, body.getTier());

        return "{}";
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PurchaseDetailsDTO {
        private UUID organizationId;
        private int amount;
        private String description;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ChangePaymentTierDTO {
        private UUID organizationId;
        private PaymentTier tier;
    }

}
