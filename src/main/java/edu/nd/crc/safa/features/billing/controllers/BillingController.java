package edu.nd.crc.safa.features.billing.controllers;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.time.temporal.TemporalAdjusters;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.billing.entities.app.TransactionAppEntity;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.billing.services.TransactionService;
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
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;

@Controller
public class BillingController extends BaseController {

    private final BillingService billingService;
    private final PermissionService permissionService;
    private final TransactionService transactionService;

    public BillingController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                             BillingService billingService, PermissionService permissionService,
                             TransactionService transactionService) {
        super(resourceBuilder, serviceProvider);
        this.billingService = billingService;
        this.permissionService = permissionService;
        this.transactionService = transactionService;
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

    /**
     * Get a list of all transactions for the current user made under their personal org
     *
     * @return The transaction list
     */
    @GetMapping(AppRoutes.Billing.Transaction.ROOT)
    public List<TransactionAppEntity> getUserTransactions() {
        Organization org = getOrgById(getCurrentUser().getPersonalOrgId());
        return getTransactionsForOrg(org);
    }

    /**
     * Get a list of all transactions for the organization with the given ID
     *
     * @param orgId The ID of the organization
     * @return The transaction list
     */
    @GetMapping(AppRoutes.Billing.Transaction.BY_ORG)
    public List<TransactionAppEntity> getOrgTransactions(@PathVariable UUID orgId) {
        Organization org = getOrgById(orgId);
        return getTransactionsForOrg(org);
    }

    /**
     * Get a list of all transactions for the current user made under their personal org within the current month
     *
     * @return The transaction list
     */
    @GetMapping(AppRoutes.Billing.Transaction.MONTHLY)
    public List<TransactionAppEntity> getMonthlyUserTransactions() {
        Organization org = getOrgById(getCurrentUser().getPersonalOrgId());
        return getMonthlyTransactionsForOrg(org);
    }

    /**
     * Get a list of all transactions for the organization with the given ID within the current month
     *
     * @param orgId The ID of the organization
     * @return The transaction list
     */
    @GetMapping(AppRoutes.Billing.Transaction.BY_ORG_MONTHLY)
    public List<TransactionAppEntity> getMonthlyOrgTransactions(@PathVariable UUID orgId) {
        Organization org = getOrgById(orgId);
        return getMonthlyTransactionsForOrg(org);
    }

    private Organization getOrgById(UUID organizationId) {
        SafaUser user = getCurrentUser();
        return getResourceBuilder().fetchOrganization(organizationId)
            .asUser(user)
            .withPermission(OrganizationPermission.VIEW_BILLING)
            .get();
    }

    private List<TransactionAppEntity> getTransactionsForOrg(Organization organization) {
        return transactionService.getOrgTransactions(organization)
            .stream().map(TransactionAppEntity::new).toList();
    }

    private List<TransactionAppEntity> getMonthlyTransactionsForOrg(Organization organization) {
        LocalDateTime startOfMonth = LocalDateTime.now()
            .with(TemporalAdjusters.firstDayOfMonth())
            .truncatedTo(ChronoUnit.DAYS);

        return transactionService.getOrgTransactionsAfter(organization, startOfMonth)
            .stream().map(TransactionAppEntity::new).toList();
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
