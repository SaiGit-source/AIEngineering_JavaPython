# NutriOpt Custom MCP Server

## 1. Project Overview

**NutriOpt Custom MCP Server** is a Spring Boot based Model Context Protocol (MCP) server designed for an AI-assisted diet optimization system. The server exposes custom tools that help an AI agent collect food price data, store nutrition and price information in MariaDB, and run a Linear Programming optimization model to produce a cost-aware daily diet plan.

The project is part of the larger **NutriOpt / DieticianAgent** system.

The high-level goal is:

> Given a user’s dietary goals, available foods, nutrition data, and price information, the AI agent should create an optimized one-day diet plan that satisfies macro targets while minimizing cost.

The custom MCP server is not responsible for natural language reasoning by itself. Instead, it exposes backend tools that an MCP client or AI agent can call.

---

## 2. Current System Architecture

The planned architecture is:

```text
User prompt
→ MCP Client / DieticianAgent
→ AI creates candidate food list
→ AI calls OpenNutrition MCP Server for nutrition facts and barcode lookup
→ AI calls NutriOpt Custom MCP Server for price lookup
→ AI saves combined nutrition + price data into MariaDB
→ AI receives saved food IDs
→ AI calls LP optimizer with MacroTargets + foodIds
→ NutriOpt MCP Server reads food rows from MariaDB
→ OR-Tools solves Linear Programming model
→ AI responds with optimized daily quantities and later a 3-meal split
```

The custom MCP server is one part of this workflow. It is responsible for:

1. Looking up product price records.
2. Saving food nutrition and price data.
3. Listing or searching saved foods.
4. Running the LP diet optimizer using saved food IDs.

---

## 3. MCP Server Type

This server is a **STDIO MCP Server**, not a web/SSE MCP server.

The server is intended to be launched by an MCP client using a command like:

```json
{
  "mcpServers": {
    "nutriopt-custom": {
      "command": "java",
      "args": [
        "--enable-native-access=ALL-UNNAMED",
        "-jar",
        "target/MCPServer-0.0.1-SNAPSHOT.jar"
      ]
    }
  }
}
```

The `--enable-native-access=ALL-UNNAMED` argument is required or recommended because the project uses Google OR-Tools, which loads native libraries.

During early testing, the server was run through MCP Inspector:

```cmd
set DANGEROUSLY_OMIT_AUTH=true
npx @modelcontextprotocol/inspector java --enable-native-access=ALL-UNNAMED -jar target\MCPServer-0.0.1-SNAPSHOT.jar
```

---

## 4. Package Structure

The main package is:

```text
com.nutriopt.MCPServer
```

The main class is:

```java
com.nutriopt.MCPServer.McpServerApplication
```

Suggested package layout:

```text
src/main/java/com/nutriopt/MCPServer
│
├── McpServerApplication.java
│
├── config
│   └── McpServerConfig.java
│
├── tools
│   ├── PingTool.java
│   ├── OpenPricesTool.java
│   ├── FoodStorageTool.java
│   └── LpOptimizerTool.java
│
├── service
│   └── LpSolverService.java
│
├── repo
│   └── FoodItemRepo.java
│
├── model
│   └── FoodItem.java
│
└── dto
    ├── MacroTargets.java
    ├── DietOptimizationRequest.java
    ├── DietOptimizationResult.java
    ├── OptimizedFoodItem.java
    ├── SaveFoodItemRequest.java
    └── SavedFoodItemResponse.java
```

---

## 5. Main Dependencies

The project uses the following important dependencies.


---

## 5A. Spring Dependencies Used in This MCP Server

This project is built on Spring Boot and several Spring ecosystem dependencies. The most important Spring dependencies are listed below.

### 5A.1 Spring Boot Starter Parent

The project uses Spring Boot as the base application framework.

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.4.5</version>
    <relativePath/>
</parent>
```

Purpose:

- Provides Spring Boot dependency management.
- Provides default Maven plugin configuration.
- Simplifies version compatibility between Spring dependencies.
- Helps create an executable Spring Boot JAR.

---

### 5A.2 Spring AI BOM

The Spring AI BOM manages compatible Spring AI dependency versions.

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-bom</artifactId>
            <version>${spring-ai.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Current version:

```text
Spring AI 1.0.0
```

Purpose:

- Keeps Spring AI modules version-aligned.
- Avoids manually specifying versions for Spring AI starters.
- Helps prevent MCP starter compatibility issues.

---

### 5A.3 Spring AI MCP Server Starter

This is the key dependency for exposing Spring methods as MCP tools.

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server</artifactId>
</dependency>
```

Purpose:

- Enables the application to run as an MCP server.
- Supports STDIO MCP mode.
- Detects `ToolCallbackProvider` beans.
- Exposes `@Tool` annotated methods to MCP clients.
- Allows tools like `ping`, `saveFoodItems`, and `optimizeDietLp` to appear in MCP Inspector.

Important decision:

```text
Use spring-ai-starter-mcp-server, not spring-ai-starter-mcp-server-webflux.
```

Reason:

```text
This project is a STDIO MCP server, not an SSE/WebFlux MCP server.
```

---

### 5A.4 Spring Boot Starter WebFlux

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

Purpose in this project:

- Provides `WebClient`.
- Used by `OpenPricesTool` to call the Open Prices API.
- Allows non-blocking HTTP requests.

Current use case:

```text
OpenPricesTool
→ WebClient
→ Open Prices API
→ price records by product_code/barcode
```

Important note:

Even though WebFlux is included for `WebClient`, the MCP server itself is still run as STDIO:

```properties
spring.main.web-application-type=none
spring.ai.mcp.server.stdio=true
```

So WebFlux is not being used to expose the MCP server over HTTP.

---

### 5A.5 Spring Boot Starter Data JPA

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

Purpose in this project:

- Provides Spring Data repositories.
- Provides JPA/Hibernate support.
- Allows `FoodItem` records to be saved in MariaDB.
- Enables `FoodItemRepo extends JpaRepository<FoodItem, Long>`.

Used by:

```text
FoodStorageTool
listSavedFoods
findSavedFoodsByName
LpOptimizerTool
```

Main repository:

```java
public interface FoodItemRepo extends JpaRepository<FoodItem, Long> {
    Optional<FoodItem> findByBarcode(String barcode);
    List<FoodItem> findByNameContainingIgnoreCase(String name);
    List<FoodItem> findByGenericNameContainingIgnoreCase(String genericName);
}
```

JPA is needed because the LP optimizer receives only food IDs, then reads the full food rows from MariaDB.

---

### 5A.6 Spring Boot Starter Validation

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

Purpose:

- Provides Bean Validation support.
- Can be used for DTO validation.
- Useful for validating required fields in future versions of:
  - `SaveFoodItemRequest`
  - `DietOptimizationRequest`
  - `MacroTargets`

Possible future examples:

```java
@NotBlank
private String name;

@NotNull
private Double caloriesPer100g;

@PositiveOrZero
private Double costPer100g;
```

Currently, validation is included to support cleaner request validation as the project grows.

---

### 5A.7 Spring Boot Starter Test

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

Purpose:

- Provides JUnit testing support.
- Provides Spring Boot test utilities.
- Can be used later to test:
  - tool registration
  - repository operations
  - LP optimizer output
  - service layer logic

During development, builds were sometimes run with:

```cmd
mvn clean package -DskipTests
```

because test failures were blocking MCP server packaging while the server was still being built.

---

### 5A.8 Reactor Test

```xml
<dependency>
    <groupId>io.projectreactor</groupId>
    <artifactId>reactor-test</artifactId>
    <scope>test</scope>
</dependency>
```

Purpose:

- Supports testing Reactor/WebFlux behavior.
- Useful for testing `WebClient`-based code later.
- Mainly relevant for `OpenPricesTool`.

---

### 5A.9 Spring Boot Maven Plugin

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
</plugin>
```

Purpose:

- Packages the project into an executable Spring Boot JAR.
- Produces:

```text
target/MCPServer-0.0.1-SNAPSHOT.jar
```

This JAR is what MCP Inspector and MCP clients launch through STDIO.

Example:

```cmd
java --enable-native-access=ALL-UNNAMED -jar target\MCPServer-0.0.1-SNAPSHOT.jar
```

---

### 5A.10 How the Spring Pieces Work Together

```text
Spring Boot
→ starts the application

Spring AI MCP Server
→ exposes ToolCallbackProvider tools over STDIO MCP

McpServerConfig
→ registers PingTool, OpenPricesTool, FoodStorageTool, LpOptimizerTool

Spring WebFlux
→ gives WebClient to OpenPricesTool

Spring Data JPA
→ gives FoodItemRepo for MariaDB reads/writes

MariaDB Driver
→ connects the app to nutriopt_db

OR-Tools
→ solves the Linear Programming optimization problem

Lombok
→ generates getters/setters for model classes
```

Overall Spring dependency role:

```text
Spring Boot = application foundation
Spring AI MCP = MCP tool server layer
Spring WebFlux = external API client layer
Spring Data JPA = persistence layer
Spring Validation = DTO validation layer
Spring Boot Test/Reactor Test = testing layer
```


### Spring Boot

Used as the application framework.

Version used:

```text
Spring Boot 3.4.5
```

### Java

During stable testing, Java 21 was preferred.

```text
Java 21
```

Java 22 caused extra uncertainty during MCP debugging, especially around native access warnings.

### Spring AI MCP Server Starter

Used to expose Java methods as MCP tools.

Dependency:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server</artifactId>
</dependency>
```

Important decision:

> Use `spring-ai-starter-mcp-server`, not `spring-ai-starter-mcp-server-webflux`, because this project uses STDIO MCP.

### WebFlux

Used for `WebClient` in `OpenPricesTool`.

Dependency:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

### Spring Data JPA

Used to persist food items in MariaDB.

Dependency:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

### MariaDB Driver

Used for database connectivity.

Dependency:

```xml
<dependency>
    <groupId>org.mariadb.jdbc</groupId>
    <artifactId>mariadb-java-client</artifactId>
    <scope>runtime</scope>
</dependency>
```

### Lombok

Used for model getters and setters.

Dependency:

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <optional>true</optional>
</dependency>
```

### Google OR-Tools

Used to solve the Linear Programming diet optimization problem.

Dependency:

```xml
<dependency>
    <groupId>com.google.ortools</groupId>
    <artifactId>ortools-java</artifactId>
    <version>9.15.6755</version>
</dependency>
```

Important note:

> OR-Tools loads native libraries. Therefore, `Loader.loadNativeLibraries()` must not be called in a static block or during Spring startup. It should be lazily loaded inside the LP solve method.

---

## 6. Application Properties

Current DB-enabled MCP configuration:

```properties
spring.application.name=MCPServer

spring.datasource.url=jdbc:mariadb://localhost:3306/nutriopt_db
spring.datasource.username=root
spring.datasource.password=maria
spring.datasource.driver-class-name=org.mariadb.jdbc.Driver
spring.datasource.hikari.connection-timeout=5000

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.format_sql=false
spring.jpa.database-platform=org.hibernate.dialect.MariaDBDialect

spring.ai.mcp.server.name=nutriopt-mcp-server
spring.ai.mcp.server.version=0.0.1
spring.ai.mcp.server.type=SYNC
spring.ai.mcp.server.stdio=true

spring.main.web-application-type=none
spring.main.banner-mode=off

logging.level.root=OFF
```

STDIO MCP requires clean output. Therefore, logging is disabled:

```properties
logging.level.root=OFF
```

During debugging, logs can be turned on temporarily, but they should be turned off for STDIO testing.

---

## 7. MCP Tool Registration

Tools are registered through `ToolCallbackProvider`.

Current tool config:

```java
package com.nutriopt.MCPServer.config;

import com.nutriopt.MCPServer.tools.FoodStorageTool;
import com.nutriopt.MCPServer.tools.LpOptimizerTool;
import com.nutriopt.MCPServer.tools.OpenPricesTool;
import com.nutriopt.MCPServer.tools.PingTool;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class McpServerConfig {

    @Bean
    public ToolCallbackProvider toolCallbackProvider(
            PingTool pingTool,
            OpenPricesTool openPricesTool,
            FoodStorageTool foodStorageTool,
            LpOptimizerTool lpOptimizerTool
    ) {
        return MethodToolCallbackProvider.builder()
                .toolObjects(
                        pingTool,
                        openPricesTool,
                        foodStorageTool,
                        lpOptimizerTool
                )
                .build();
    }
}
```

The tools are Java Spring beans annotated with `@Component` or `@Service`, and their MCP-callable methods are annotated with `@Tool`.

---

## 8. Tools Implemented

### 8.1 `ping`

Purpose:

Simple connectivity test.

Tool behavior:

```text
Input: none
Output: "pong"
```

This tool was used to confirm that:

1. Spring AI MCP STDIO worked.
2. MCP Inspector could connect.
3. Tool registration worked.
4. The issue was not the MCP protocol itself.

---

### 8.2 `getOpenPricesByProductCode`

Purpose:

Calls the Open Prices API using a product barcode or product code.

Input:

```json
{
  "productCode": "055577105026"
}
```

Example test:

```json
{
  "productCode": "quaker oats"
}
```

Observed result:

```json
{
  "items": [],
  "page": 1,
  "pages": 1,
  "size": 10,
  "total": 0
}
```

Important concept:

- Open Prices uses `product_code`.
- For packaged foods, this should usually be a barcode.
- Generic foods like `"oats"` do not have one universal barcode.
- Branded foods like Quaker oats can have product-specific barcodes.
- Open Prices is crowdsourced and may not always return prices.
- If Open Prices returns no results, the system can use manual fallback prices.

---

### 8.3 `saveFoodItems`

Purpose:

Saves one or more food items into MariaDB.

It stores:

- Food name
- Generic name
- Brand
- Barcode
- Quantity text
- Package size
- Nutrition per 100g
- Latest price
- Currency
- Cost per 100g
- Price source
- Price date
- Minimum grams
- Maximum grams

Input shape:

```json
[
  {
    "name": "Quaker Large Flake Oats",
    "genericName": "oats",
    "brand": "Quaker",
    "barcode": "055577105026",
    "quantityText": "1 kg",
    "packageSizeGrams": 1000.0,
    "caloriesPer100g": 389.0,
    "proteinPer100g": 16.9,
    "carbsPer100g": 66.3,
    "fatPer100g": 6.9,
    "fiberPer100g": 10.6,
    "latestPrice": 4.99,
    "currency": "CAD",
    "costPer100g": 0.499,
    "priceSource": "manual_test",
    "priceDate": "2026-06-08",
    "minGrams": 30.0,
    "maxGrams": 150.0
  }
]
```

Behavior:

- If barcode already exists, update the existing item.
- Otherwise, insert a new item.
- Return saved food IDs and summary information.

---

### 8.4 `listSavedFoods`

Purpose:

Lists all saved food items from MariaDB.

This tool is important because the LP optimizer does not receive full food data directly. It receives only `foodIds`.

Workflow:

```text
saveFoodItems
→ listSavedFoods
→ copy IDs
→ optimizeDietLp
```

---

### 8.5 `findSavedFoodsByName`

Purpose:

Searches saved food items by food name.

Use cases:

- Check whether a food is already saved.
- Avoid duplicate foods.
- Find a food ID before optimization.

---

### 8.6 `optimizeDietLp`

Purpose:

Runs the Linear Programming diet optimizer.

Input shape:

```json
{
  "foodIds": [1, 2, 3, 4, 5, 6, 7, 8],
  "targets": {
    "budgetMax": 100,
    "caloriesMax": 10000,
    "caloriesMin": 500,
    "carbsMax": 1000,
    "carbsMin": 0,
    "fatMax": 500,
    "fatMin": 0,
    "fiberMin": 0,
    "proteinMin": 0
  }
}
```

Output example:

```json
{
  "status": "OPTIMAL",
  "totalCalories": 2000,
  "totalProtein": 100,
  "totalCarbs": 273.19,
  "totalFat": 58.03,
  "totalFiber": 27.76,
  "totalCost": 4.6,
  "items": [
    {
      "foodId": 1,
      "food": "Quaker Large Flake Oats",
      "quantity": 150,
      "unit": "g/ml"
    },
    {
      "foodId": 2,
      "food": "Whole Milk 3.25%",
      "quantity": 220.8,
      "unit": "g/ml"
    }
  ]
}
```

Test result confirmed:

```text
status: OPTIMAL
```

This confirms:

```text
MariaDB saved foods
→ food IDs passed to optimizer
→ LpOptimizerTool reads FoodItem rows
→ OR-Tools solves LP
→ MCP tool returns optimized diet quantities
```

---

## 9. Linear Programming Model

The optimization problem is a one-day diet planning LP.

### 9.1 Decision Variables

Let:

```text
x_i = daily quantity of food i in grams or ml
```

For each food item \(i\):

```math
x_i \geq 0
```

Each food has a lower and upper bound:

```math
L_i \leq x_i \leq U_i
```

where:

- \(L_i\) = minimum grams/ml per day
- \(U_i\) = maximum grams/ml per day

These are stored in MariaDB as:

```text
minGrams
maxGrams
```

---

### 9.2 Nutrient Coefficients

Each food stores nutrition per 100g:

```text
caloriesPer100g
proteinPer100g
carbsPer100g
fatPer100g
fiberPer100g
costPer100g
```

For each food \(i\), convert per-100g values into per-gram values:

```math
cal_i = \frac{caloriesPer100g_i}{100}
```

```math
p_i = \frac{proteinPer100g_i}{100}
```

```math
c_i = \frac{carbsPer100g_i}{100}
```

```math
f_i = \frac{fatPer100g_i}{100}
```

```math
r_i = \frac{fiberPer100g_i}{100}
```

```math
k_i = \frac{costPer100g_i}{100}
```

where:

- \(cal_i\) = calories per gram
- \(p_i\) = protein per gram
- \(c_i\) = carbs per gram
- \(f_i\) = fat per gram
- \(r_i\) = fiber per gram
- \(k_i\) = cost per gram

---

### 9.3 Objective Function

The current objective is:

> Minimize total daily cost.

```math
\min \sum_{i=1}^{n} k_i x_i
```

where:

- \(k_i\) = cost per gram of food \(i\)
- \(x_i\) = selected grams/ml of food \(i\)

---

### 9.4 Calorie Constraint

The diet must fall between minimum and maximum calories:

```math
Calories_{min} \leq \sum_{i=1}^{n} cal_i x_i \leq Calories_{max}
```

---

### 9.5 Protein Constraint

The diet must provide at least the minimum protein:

```math
\sum_{i=1}^{n} p_i x_i \geq Protein_{min}
```

---

### 9.6 Carbohydrate Constraint

The diet must fall between minimum and maximum carbs:

```math
Carbs_{min} \leq \sum_{i=1}^{n} c_i x_i \leq Carbs_{max}
```

---

### 9.7 Fat Constraint

The diet must fall between minimum and maximum fat:

```math
Fat_{min} \leq \sum_{i=1}^{n} f_i x_i \leq Fat_{max}
```

---

### 9.8 Fiber Constraint

The diet must provide at least the minimum fiber:

```math
\sum_{i=1}^{n} r_i x_i \geq Fiber_{min}
```

---

### 9.9 Budget Constraint

The diet must not exceed the maximum daily budget:

```math
\sum_{i=1}^{n} k_i x_i \leq Budget_{max}
```

Since the objective already minimizes cost, the budget constraint is optional mathematically, but useful for strict user limits.

---

### 9.10 Complete LP Formulation

```math
\min \sum_{i=1}^{n} k_i x_i
```

Subject to:

```math
L_i \leq x_i \leq U_i \quad \forall i
```

```math
Calories_{min} \leq \sum_{i=1}^{n} cal_i x_i \leq Calories_{max}
```

```math
\sum_{i=1}^{n} p_i x_i \geq Protein_{min}
```

```math
Carbs_{min} \leq \sum_{i=1}^{n} c_i x_i \leq Carbs_{max}
```

```math
Fat_{min} \leq \sum_{i=1}^{n} f_i x_i \leq Fat_{max}
```

```math
\sum_{i=1}^{n} r_i x_i \geq Fiber_{min}
```

```math
\sum_{i=1}^{n} k_i x_i \leq Budget_{max}
```

---

## 10. Solver Used

The current OR-Tools solver is:

```java
MPSolver solver = MPSolver.createSolver("GLOP");
```

`GLOP` is a linear programming solver.

The result status can be:

```text
OPTIMAL
INFEASIBLE
UNBOUNDED
ABNORMAL
NOT_SOLVED
```

During testing, loose constraints returned:

```text
OPTIMAL
```

Stricter constraints returned:

```text
INFEASIBLE
```

This was expected because the selected foods and their min/max gram constraints may not be able to satisfy all macro requirements at once.

---

## 11. OR-Tools Startup Issue and Fix

A key issue was discovered during MCP Inspector testing.

Original problematic code:

```java
@Service
public class LpSolverService {

    static {
        Loader.loadNativeLibraries();
    }
}
```

Problem:

- Static blocks run when the class loads.
- Spring loads service classes during application startup.
- OR-Tools prints native library warnings.
- STDIO MCP expects clean JSON-RPC communication.
- Warnings can pollute STDIO and break MCP Inspector tool discovery.

Fixed approach:

```java
@Service
public class LpSolverService {

    private boolean ortoolsLoaded = false;

    private void ensureOrToolsLoaded() {
        if (!ortoolsLoaded) {
            Loader.loadNativeLibraries();
            ortoolsLoaded = true;
        }
    }

    public DietOptimizationResult solve(MacroTargets targets, List<FoodItem> foods) {
        ensureOrToolsLoaded();

        // solve LP here
    }
}
```

Also, run the server with:

```cmd
java --enable-native-access=ALL-UNNAMED -jar target\MCPServer-0.0.1-SNAPSHOT.jar
```

or through Inspector:

```cmd
set DANGEROUSLY_OMIT_AUTH=true
npx @modelcontextprotocol/inspector java --enable-native-access=ALL-UNNAMED -jar target\MCPServer-0.0.1-SNAPSHOT.jar
```

---

## 12. Debugging Timeline and Lessons Learned

### 12.1 PingTool Baseline

A separate minimal MCP project was created with only:

```text
PingTool
McpServerConfig
spring-ai-starter-mcp-server
STDIO properties
```

This confirmed that:

```text
Spring AI MCP STDIO works
MCP Inspector works
ToolCallbackProvider registration works
```

### 12.2 Original NutriOpt Server Debugging

The original NutriOpt project initially failed to list tools because multiple services and dependencies were active at once.

Issues encountered:

1. Missing or moved Java files.
2. POM was temporarily changed to a minimal PingTool POM.
3. Tools had missing imports after dependencies were removed.
4. DTO/model files were missing after disabling/restoring files.
5. OR-Tools loaded at startup and produced native access warnings.
6. MariaDB/JPA dependencies had to be restored.
7. Tool registration had to be tested one tool at a time.

### 12.3 Successful Incremental Testing Order

The successful order was:

```text
1. PingTool only
2. PingTool + OpenPricesTool
3. Add FoodStorageTool
4. Add listSavedFoods and findSavedFoodsByName
5. Save foods into MariaDB
6. Add LpOptimizerTool
7. Fix OR-Tools lazy loading
8. Run optimizeDietLp
9. Confirm OPTIMAL result
```

---

## 13. Current Working Status

The following tools are now visible in MCP Inspector:

```text
ping
getOpenPricesByProductCode
saveFoodItems
listSavedFoods
findSavedFoodsByName
optimizeDietLp
```

Confirmed working:

```text
PingTool → returns "pong"
OpenPricesTool → calls Open Prices API
FoodStorageTool → saves food items into MariaDB
listSavedFoods → lists saved foods with IDs
findSavedFoodsByName → searches saved foods
LpOptimizerTool → calls OR-Tools through LpSolverService
optimizeDietLp → returns OPTIMAL for loose constraints
```

---

## 14. Example Food Save Payload

Example payload for `saveFoodItems`:

```json
[
  {
    "name": "Quaker Large Flake Oats",
    "genericName": "oats",
    "brand": "Quaker",
    "barcode": "055577105026",
    "quantityText": "1 kg",
    "packageSizeGrams": 1000.0,
    "caloriesPer100g": 389.0,
    "proteinPer100g": 16.9,
    "carbsPer100g": 66.3,
    "fatPer100g": 6.9,
    "fiberPer100g": 10.6,
    "latestPrice": 4.99,
    "currency": "CAD",
    "costPer100g": 0.499,
    "priceSource": "manual_test",
    "priceDate": "2026-06-08",
    "minGrams": 30.0,
    "maxGrams": 150.0
  }
]
```

---

## 15. Example LP Optimizer Payload

Loose test payload:

```json
{
  "foodIds": [1, 2, 3, 4, 5, 6, 7, 8],
  "targets": {
    "budgetMax": 100,
    "caloriesMax": 10000,
    "caloriesMin": 500,
    "carbsMax": 1000,
    "carbsMin": 0,
    "fatMax": 500,
    "fatMin": 0,
    "fiberMin": 0,
    "proteinMin": 0
  }
}
```

Stricter bulking payload:

```json
{
  "foodIds": [1, 2, 3, 4, 5, 6, 7, 8],
  "targets": {
    "budgetMax": 20,
    "caloriesMax": 3000,
    "caloriesMin": 2000,
    "carbsMax": 450,
    "carbsMin": 180,
    "fatMax": 130,
    "fatMin": 40,
    "fiberMin": 15,
    "proteinMin": 100
  }
}
```

If the stricter payload returns `INFEASIBLE`, then the food list, macro bounds, or min/max food gram constraints need adjustment.

---

## 16. Planned MCP Client / DieticianAgent

Tomorrow’s planned work is the MCP client.

The client should connect to two MCP servers:

1. **OpenNutrition MCP Server**
2. **NutriOpt Custom MCP Server**

Planned full agent workflow:

```text
User says:
"Create a cheap 2500 calorie high-protein diet using oats, milk, rice, chicken, eggs, and banana."

DieticianAgent:
1. Parses calorie, protein, budget, and food preferences.
2. Creates food candidate list.
3. Calls OpenNutrition MCP Server:
   - search food
   - get product candidates
   - get barcode
   - get nutrition per 100g
4. Calls NutriOpt Custom MCP Server:
   - getOpenPricesByProductCode
   - if no price found, use manual fallback price
   - saveFoodItems
   - listSavedFoods or use returned IDs
   - optimizeDietLp
5. Converts optimized quantities into meal format:
   - Breakfast
   - Lunch
   - Dinner
   - Optional snack
6. Returns:
   - optimized quantities
   - calories/macros
   - estimated daily cost
   - notes about missing prices or fallback assumptions
```

---

## 17. Next Planned Improvements

### 17.1 Better Infeasibility Diagnostics

When OR-Tools returns `INFEASIBLE`, the system should explain why.

Possible diagnostics:

- Total maximum calories is below `caloriesMin`.
- Total maximum protein is below `proteinMin`.
- Minimum required food amounts exceed `fatMax`.
- Minimum required food amounts exceed `carbsMax`.
- Minimum required food amounts exceed `budgetMax`.
- Food IDs are missing or empty.
- Selected foods do not contain enough protein/fiber.

### 17.2 Meal Splitting

After LP returns daily grams, split into meals:

```text
Breakfast: oats, milk, banana, peanut butter
Lunch: rice, chicken, vegetables
Dinner: eggs, rice, vegetables
Snack: milk or banana
```

This can initially be rule-based.

### 17.3 More Realistic Food Constraints

Examples:

```text
oats: 40g–120g
milk: 200ml–600ml
eggs: 50g–200g
chicken: 100g–350g
rice: 100g–500g
banana: 80g–250g
peanut butter: 10g–50g
vegetables: 100g–500g
```

### 17.4 Multiple Objective Modes

Current:

```text
minimize cost
```

Future objective options:

```text
minimize cost
maximize protein per dollar
minimize deviation from preferred foods
minimize cooking complexity
maximize variety
```

### 17.5 Integration with OpenNutrition MCP Server

The MCP client should ask OpenNutrition for:

```text
food search
nutrition facts
barcode/product code
brand information
serving size
```

Then ask NutriOpt MCP Server for:

```text
price lookup
saving food data
LP optimization
```

---

## 18. Current Run Commands

Build:

```cmd
mvn clean package -DskipTests
```

Run with MCP Inspector:

```cmd
set DANGEROUSLY_OMIT_AUTH=true
npx @modelcontextprotocol/inspector java --enable-native-access=ALL-UNNAMED -jar target\MCPServer-0.0.1-SNAPSHOT.jar
```

If ports conflict:

```cmd
set DANGEROUSLY_OMIT_AUTH=true
set CLIENT_PORT=6284
set SERVER_PORT=6287
npx @modelcontextprotocol/inspector java --enable-native-access=ALL-UNNAMED -jar target\MCPServer-0.0.1-SNAPSHOT.jar
```

---

## 19. Final Current Status

The custom NutriOpt MCP Server is now functioning as a backend MCP tool server.

Working confirmed:

```text
STDIO MCP server starts
MCP Inspector connects
Tools are listed
Ping works
OpenPrices works
MariaDB save/list/search works
OR-Tools LP optimizer works
OPTIMAL result confirmed
```

Next task:

> Build the MCP Client / DieticianAgent that connects to both OpenNutrition MCP Server and this NutriOpt MCP Server, then revise this document with the full client architecture.
