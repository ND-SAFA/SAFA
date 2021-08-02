package edu.nd.crc.safa.importer.flatfile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.importer.MySQL;
import edu.nd.crc.safa.responses.FlatFileResponse;

import com.jsoniter.JsonIterator;
import com.jsoniter.spi.JsonException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;


@Component
/* Responsible for reading and parsing flat files.
 * A flat file describes some part of a project's
 * Traceability Information Model (TIM).
 */
public class UploadFlatFile {


    private MySQL sql;
    private FlatFileParser flatFileParser;

    @Autowired
    public UploadFlatFile(MySQL sql, FlatFileParser flatFileParser) {
        this.sql = sql;
        this.flatFileParser = flatFileParser;
    }

    public FlatFileResponse uploadFiles(String projectId, String jsonfiles) throws ServerError {
        OSHelper.clearOrCreateDirectory(ProjectPaths.PATH_TO_FLAT_FILES);

        try {
            JsonIterator iterator = JsonIterator.parse(jsonfiles);
            for (String filename = iterator.readObject(); filename != null; filename = iterator.readObject()) {
                String encodedData = iterator.readString();
                byte[] bytes = Base64.getDecoder().decode(encodedData);
                String fullPath = ProjectPaths.PATH_TO_FLAT_FILES + "/" + filename;
                Files.write(Paths.get(fullPath), bytes);

                if (filename.equals("tim.json")) {
                    sql.clearTimTables();
                    flatFileParser.parseTimFile(fullPath);
                } else {
                    flatFileParser.parseRegularFile(filename, fullPath);
                }
            }
        } catch (IOException e) {
            throw new ServerError("uploading files", e);
        } catch (JsonException e) {
            throw new ServerError("parsing json file", e);
        }

        sql.traceArtifactCheck();
        MySQL.FileInfo fileInfo = sql.getFileInfo();

        return new FlatFileResponse(fileInfo.uploadedFiles,
            fileInfo.expectedFiles,
            fileInfo.generatedFiles,
            fileInfo.expectedGeneratedFiles
        );
    }
}
