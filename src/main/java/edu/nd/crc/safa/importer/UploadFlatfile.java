package edu.nd.crc.safa.importer;

import java.util.ArrayList;
import java.util.List;
import java.util.Base64;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.BufferedReader;
import java.io.FileReader;


import com.jsoniter.JsonIterator;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class UploadFlatfile {
  @Autowired private MySQL sql = new MySQL();
  
  public static class TimBackend {
    public List<List<String>> artifacts = new ArrayList<List<String>>();
    public List<List<String>> traces = new ArrayList<List<String>>();
  }

  public String uploadFiles(String projId, String jsonfiles) throws Exception {
    String path = "/uploadedFlatfiles";
    createDirectory(path);
    
    JsonIterator iterator = JsonIterator.parse(jsonfiles);
    for (String filename = iterator.readObject(); filename != null; filename = iterator.readObject()) {
      String encodedData = iterator.readString();
      byte[] bytes = Base64.getDecoder().decode(encodedData);
      String fullPath = path + "/" + filename; 
      Files.write(Paths.get(fullPath), bytes);
      
      if (filename.equals("tim.json")) {
        sql.clearTimTables();
        parseTimFile(fullPath);
      } else {
        parseRegFile(filename, fullPath);
      }
    }

    sql.traceArtifactCheck();
    MySQL.FileInfo fileInfo = sql.getFileInfo();

    String data = "{\"uploadedFiles\":" + fileInfo.uploadedFiles.toString() + ",\"expectedFiles\":" +
                  fileInfo.expectedFiles.toString() + ",\"generatedFiles\":" + fileInfo.generatedFiles.toString() +
                  ",\"expectedGeneratedFiles\":" + fileInfo.expectedGeneratedFiles.toString() + "}";
    
    System.out.println(data);
    return String.format("{ \"success\": true, \"message\": \"Checking missing files successful.\", \"data\": %s }", data);
  }

  public void parseTimFile(String fullPath) throws Exception {
    String data = new String(Files.readAllBytes(Paths.get(fullPath)));
    JsonIterator iterator = JsonIterator.parse(data);

    for (String field = iterator.readObject(); field != null; field = iterator.readObject()){
      if (field.toLowerCase().equals("datafiles")) {
        for (String artifactName = iterator.readObject(); artifactName != null; artifactName = iterator.readObject()){
          String fileName = "";

          for (String field2 = iterator.readObject(); field2 != null; field2 = iterator.readObject()){
            if (!field2.toLowerCase().equals("file")){
              throw new Exception(String.format("Artifact: %s. Expected File attribute. The File attribute should appear as 'File': 'FileName'", artifactName));
            }

            fileName = iterator.readString();
          }

          if (fileName.isEmpty()) {
            throw new Exception(String.format("Did not provide a File for Artifact: %s. The File attribute should appear as 'File': 'FileName.csv'", artifactName));
          }

          String artifactTableName = fileName.replaceAll("(?i)\\.csv","").toLowerCase();
          sql.createTimArtifactsTable(artifactName, artifactTableName, fileName);
        }
      }
      else {
        parseTraceMatrix(field, iterator);
      }
    }
  }

  public void parseRegFile(String filename, String fullPath) throws Exception {
    try (BufferedReader uploadedFileReader = new BufferedReader(new FileReader(fullPath))) {
      String[] headers = uploadedFileReader.readLine().split(",");

      if (headers.length == 2) {
        Boolean source = false;
        Boolean target = false;
        List<String> cols = new ArrayList<String>();

        for (String header : headers) {
          if (header.toLowerCase().equals("source")) {
            source = true;
            cols.add("source_id");
          }
          else if (header.toLowerCase().equals("target")) {
            target = true;
            cols.add("target_id");
          }
        }

        if (source && target) {
          String tableName = filename.replaceAll("(?i)\\.csv","").toLowerCase();
          String colHeader = cols.toString().replace("[","(").replace("]", ")");
          sql.createTraceMatrixTable(tableName,fullPath, colHeader);
        }        
      }
      else if (headers.length == 3) {
        Boolean id = false;
        Boolean summary = false;
        Boolean content = false;
        List<String> cols = new ArrayList<String>();

        for (String header : headers) {
          if (header.toLowerCase().equals("id")) {
            id = true;
            cols.add("id");
          }
          else if (header.toLowerCase().equals("summary")) {
            summary = true;
            cols.add("summary");
          }
          else if (header.toLowerCase().equals("content")) {
            content = true;
            cols.add("content");
          }
        }

        if (id && summary && content) {
          String tableName = filename.replaceAll("(?i)\\.csv","").toLowerCase();
          String colHeader = cols.toString().replace("[","(").replace("]", ")");
          sql.createArtifactTable(tableName,fullPath, colHeader);
        }
      }
      else {
        System.out.println(String.format("Do not recognize file: %s", filename));
      }
    }
  }

  public void parseTraceMatrix(String tracename, JsonIterator iterator) throws Exception {
    String filename = "";
    String source = "";
    String target = "";
    Boolean generated = false;

    for (String attr = iterator.readObject(); attr != null; attr = iterator.readObject()) {
      if (!attr.toLowerCase().matches("file|source|target|generatelinks")) {
        throw new Exception(String.format("LinkFile: %s Attribute: %s does not match expected: 'File', 'Source', 'Target', or 'generateLinks'", tracename, attr));
      }

      if (attr.toLowerCase().equals("file")){
        filename = iterator.readString();
      }

      if (attr.toLowerCase().equals("source")){
        source = iterator.readString();
      }

      if (attr.toLowerCase().equals("target")){
        target = iterator.readString();
      }

      if (attr.toLowerCase().equals("generatelinks")){
        generated = iterator.readString().toLowerCase().equals("true") ? true : false;
      }
    }

    if (source.isEmpty()) {
      throw new Exception(String.format("Missing attribute for: '%s'. Missing: 'Source' Required attributes are 'File', 'Source', 'Target'", tracename));
    }

    if (target.isEmpty()) {
      throw new Exception(String.format("Missing attribute for: '%s'. Missing: 'Target' Required attributes are 'File', 'Source', 'Target'", tracename));
    }

    if (!generated && filename.isEmpty()) {
      throw new Exception(String.format("Missing attribute for: '%s'. Missing: 'File' Required attributes are 'File', 'Source', 'Target'", tracename));
    }

    if (generated && !filename.isEmpty()) {
      throw new Exception(String.format("Link: %s is a generated file and does not have a File attribute. Please delete the link attribute 'File: %s' or remove 'generateLinks: True'.", tracename, filename));
    }

    if (generated) {
      String traceMatrixTableName = tracename.toLowerCase();
      sql.createTimTraceMatrixTable(tracename, traceMatrixTableName, source, target, generated, tracename);
    }
    else {
      String traceMatrixTableName = filename.replaceAll("(?i)\\.csv","").toLowerCase();
      sql.createTimTraceMatrixTable(tracename, traceMatrixTableName, source, target, generated, filename);
    }
  }

  public static File createDirectory(String dir) throws Exception {
    File myDir = new File(dir);

    if (!myDir.exists()) {
      if (!myDir.mkdirs()){
        throw new Exception(String.format("Error creating folder: Path: %s", dir));
      }
    }

    if (!myDir.isDirectory()) {
      if (!myDir.delete()){
        throw new Exception(String.format("Error deleting file: Path: %s", dir));
      }
      if (!myDir.mkdirs()){
        throw new Exception(String.format("Error creating folder: Path: %s", dir));
      }
    }

    return myDir;
  }

  public static void deleteDirectory(String dir) throws Exception {
    File myDir = new File(dir);
    
    if (myDir.isDirectory()) {
      deleteDirectoryHelper(myDir);
    }
  }

  public static boolean deleteDirectoryHelper(File dir) throws Exception {
    File[] files = dir.listFiles();
    if (files != null) {
      for (File file : files) {
        deleteDirectoryHelper(file);
      }
    }
    return dir.delete();
  }

  public TimBackend getTimFile() throws Exception {
    TimBackend timBackend = new TimBackend();

    List<List<String>> artifact_rows = sql.getTimArtifactData();
    for (List<String> artifact_row : artifact_rows) {
      List<String> artifacts = new ArrayList<String>();
      
      String artifact  = String.format("\"%s\"",artifact_row.get(0));
      String filename  = String.format("\"%s\"",artifact_row.get(2));

      artifacts.add(artifact);
      artifacts.add(filename);
      timBackend.artifacts.add(artifacts);
    }

    List<List<String>> trace_rows = sql.getTimTraceData();
    for (List<String> trace_row : trace_rows) {
      List<String> traces = new ArrayList<String>();
      
      String trace  = String.format("\"%s\"",trace_row.get(0));
      String source  = String.format("\"%s\"",trace_row.get(1));
      String target  = String.format("\"%s\"",trace_row.get(2));
      String filename  = String.format("\"%s\"",trace_row.get(5));

      if (trace_rows.get(3).equals('1')) {
        filename  = String.format("\"generateLinks\"");
      }

      traces.add(trace);
      traces.add(source);
      traces.add(target);
      traces.add(filename);

      timBackend.traces.add(traces);
    }

    return timBackend;
  }
}