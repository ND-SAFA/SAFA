package edu.nd.crc.safa.server.controllers;

import java.util.HashMap;
import java.util.Map;

import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.Warning;
import edu.nd.crc.safa.server.db.repositories.ProjectRepository;
import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.db.repositories.WarningRepository;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.services.WarningService;
import edu.nd.crc.safa.warnings.Rule;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class WarningController extends BaseController {

    WarningService warningService;
    WarningRepository warningRepository;

    @Autowired
    public WarningController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             WarningService warningService,
                             WarningRepository warningRepository) {
        super(projectRepository, projectVersionRepository);
        this.warningService = warningService;
        this.warningRepository = warningRepository;
    }

    @GetMapping("projects/warnings/{projectId}")
    @Transactional(readOnly = true)
    public Map<String, String> getProjectWarnings(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        Map<String, String> result = new HashMap<String, String>();
        for (Rule r : warningService.getProjectRules(project)) {
            result.put(r.toString(), r.unprocessedRule());
        }
        return result;
    }

    @PostMapping("projects/warnings/{projectId}")
    @ResponseStatus(HttpStatus.CREATED)
    public void createNewWarning(@PathVariable String projectId,
                                 @RequestParam("short") String nShort,
                                 @RequestParam("long") String nLong,
                                 @RequestParam("rule") String rule) throws ServerError {
        Project project = getProject(projectId);
        Warning warning = new Warning(project, nShort, nLong, rule);
        this.warningRepository.save(warning);
    }
}
