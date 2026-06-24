package com.banking.rca_backend.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class DashboardService {

    private final ObjectMapper objectMapper;
    private final String logsFile;

    public DashboardService(
            ObjectMapper objectMapper,
            @Value("${dashboard.logs-file:../../data/raw_logs.jsonl}") String logsFile
    ) {
        this.objectMapper = objectMapper;
        this.logsFile = logsFile;
    }

    public Map<String, Object> getOverview() {
        List<JsonNode> logs = readLogs();

        List<JsonNode> errorLogs = logs.stream()
                .filter(log -> !"NONE".equalsIgnoreCase(log.path("errorCode").asText("NONE")))
                .toList();

        return Map.of(
                "errorCodes", countBy(errorLogs, "errorCode", "errorCode", "count"),
                "errorsByService", countBy(errorLogs, "service", "service", "errors"),
                "errorTrend", buildErrorTrend(errorLogs),
                "traces", buildTraces(errorLogs)
        );
    }

    private List<JsonNode> readLogs() {
        try {
            Path path = Path.of(logsFile);

            return Files.readAllLines(path)
                    .stream()
                    .filter(line -> !line.isBlank())
                    .map(line -> {
                        try {
                            return objectMapper.readTree(line);
                        } catch (Exception e) {
                            throw new RuntimeException("Invalid JSON log line: " + line, e);
                        }
                    })
                    .toList();

        } catch (Exception e) {
            throw new RuntimeException("Failed to read logs file: " + logsFile, e);
        }
    }

    private List<Map<String, Object>> countBy(
            List<JsonNode> logs,
            String field,
            String outputName,
            String countName
    ) {
        Map<String, Long> counts = logs.stream()
                .collect(Collectors.groupingBy(
                        log -> log.path(field).asText("unknown"),
                        LinkedHashMap::new,
                        Collectors.counting()
                ));

        return counts.entrySet()
                .stream()
                .map(entry -> {
                    Map<String, Object> row = new LinkedHashMap<>();
                    row.put(outputName, entry.getKey());
                    row.put(countName, entry.getValue());
                    return row;
                })
                .toList();
    }

    private List<Map<String, Object>> buildErrorTrend(List<JsonNode> errorLogs) {
        Map<String, Long> counts = errorLogs.stream()
                .collect(Collectors.groupingBy(
                        log -> log.path("timestamp").asText("").substring(11, 19),
                        TreeMap::new,
                        Collectors.counting()
                ));

        return counts.entrySet()
                .stream()
                .map(entry -> {
                    Map<String, Object> row = new LinkedHashMap<>();
                    row.put("time", entry.getKey());
                    row.put("errors", entry.getValue());
                    return row;
                })
                .toList();
    }

    private List<Map<String, Object>> buildTraces(List<JsonNode> errorLogs) {
        Map<String, List<JsonNode>> logsByTrace = errorLogs.stream()
                .collect(Collectors.groupingBy(log -> log.path("traceId").asText("unknown")));

        return logsByTrace.entrySet()
                .stream()
                .map(entry -> {
                    List<JsonNode> traceLogs = entry.getValue();

                    Set<String> services = traceLogs.stream()
                            .map(log -> log.path("service").asText("unknown"))
                            .collect(Collectors.toCollection(LinkedHashSet::new));

                    Set<String> errorCodes = traceLogs.stream()
                            .map(log -> log.path("errorCode").asText("NONE"))
                            .collect(Collectors.toCollection(LinkedHashSet::new));

                    Map<String, Object> row = new LinkedHashMap<>();
                    row.put("traceId", entry.getKey());
                    row.put("transactionId", traceLogs.get(0).path("transactionId").asText("unknown"));
                    row.put("services", String.join(", ", services));
                    row.put("errorCodes", String.join(", ", errorCodes));
                    row.put("severity", "High");

                    return row;
                })
                .toList();
    }
}