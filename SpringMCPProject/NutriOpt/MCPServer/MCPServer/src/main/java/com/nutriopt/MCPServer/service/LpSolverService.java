package com.nutriopt.MCPServer.service;

import com.google.ortools.Loader;
import com.google.ortools.linearsolver.MPConstraint;
import com.google.ortools.linearsolver.MPObjective;
import com.google.ortools.linearsolver.MPSolver;
import com.google.ortools.linearsolver.MPVariable;
import com.nutriopt.MCPServer.dto.DietOptimizationResult;
import com.nutriopt.MCPServer.dto.MacroTargets;
import com.nutriopt.MCPServer.dto.OptimizedFoodItem;
import com.nutriopt.MCPServer.model.FoodItem;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class LpSolverService {

    private boolean ortoolsLoaded = false;

    private void ensureOrToolsLoaded() {
        if (!ortoolsLoaded) {
            Loader.loadNativeLibraries();
            ortoolsLoaded = true;
        }
    }

    public DietOptimizationResult solve(
            MacroTargets targets,
            List<FoodItem> foods
    ) {
        ensureOrToolsLoaded();

        if (targets == null) {
            return emptyResult("INVALID_TARGETS");
        }

        if (foods == null || foods.isEmpty()) {
            return emptyResult("NO_FOODS_PROVIDED");
        }

        MPSolver solver = MPSolver.createSolver("GLOP");

        if (solver == null) {
            return emptyResult("SOLVER_NOT_AVAILABLE");
        }

        int n = foods.size();

        MPVariable[] x = new MPVariable[n];

        for (int i = 0; i < n; i++) {
            FoodItem food = foods.get(i);

            double min = valueOrDefault(food.getMinGrams(), 0.0);
            double max = valueOrDefault(food.getMaxGrams(), 1000.0);

            x[i] = solver.makeNumVar(
                    min,
                    max,
                    safeVariableName(food.getName()) + "_" + i
            );
        }

        addConstraint(
                solver,
                x,
                foods,
                valueOrDefault(targets.caloriesMin(), 0.0),
                valueOrInfinity(targets.caloriesMax()),
                "calorie_constraint",
                NutrientType.CALORIES
        );

        addConstraint(
                solver,
                x,
                foods,
                valueOrDefault(targets.proteinMin(), 0.0),
                Double.POSITIVE_INFINITY,
                "protein_constraint",
                NutrientType.PROTEIN
        );

        addConstraint(
                solver,
                x,
                foods,
                valueOrDefault(targets.carbsMin(), 0.0),
                valueOrInfinity(targets.carbsMax()),
                "carb_constraint",
                NutrientType.CARBS
        );

        addConstraint(
                solver,
                x,
                foods,
                valueOrDefault(targets.fatMin(), 0.0),
                valueOrInfinity(targets.fatMax()),
                "fat_constraint",
                NutrientType.FAT
        );

        addConstraint(
                solver,
                x,
                foods,
                valueOrDefault(targets.fiberMin(), 0.0),
                Double.POSITIVE_INFINITY,
                "fiber_constraint",
                NutrientType.FIBER
        );

        
        addConstraint(
                solver,
                x,
                foods,
                0.0,
                targets.budgetMax(),
                "budget_constraint",
                NutrientType.COST
        );

        MPObjective objective = solver.objective();

        for (int i = 0; i < n; i++) {
            FoodItem food = foods.get(i);
            double costPerGram = valueOrDefault(food.getCostPer100g(), 0.0) / 100.0;
            objective.setCoefficient(x[i], costPerGram);
        }

        objective.setMinimization();

        MPSolver.ResultStatus resultStatus = solver.solve();

        if (resultStatus != MPSolver.ResultStatus.OPTIMAL) {
            return emptyResult(resultStatus.name());
        }

        return buildResult(x, foods);
    }

    private void addConstraint(
            MPSolver solver,
            MPVariable[] variables,
            List<FoodItem> foods,
            double lowerBound,
            double upperBound,
            String constraintName,
            NutrientType nutrientType
    ) {
        MPConstraint constraint = solver.makeConstraint(
                lowerBound,
                upperBound,
                constraintName
        );

        for (int i = 0; i < foods.size(); i++) {
            double coefficient = getCoefficientPerGram(foods.get(i), nutrientType);
            constraint.setCoefficient(variables[i], coefficient);
        }
    }

    private double getCoefficientPerGram(
            FoodItem food,
            NutrientType nutrientType
    ) {
        return switch (nutrientType) {
            case CALORIES -> valueOrDefault(food.getCaloriesPer100g(), 0.0) / 100.0;
            case PROTEIN -> valueOrDefault(food.getProteinPer100g(), 0.0) / 100.0;
            case CARBS -> valueOrDefault(food.getCarbsPer100g(), 0.0) / 100.0;
            case FAT -> valueOrDefault(food.getFatPer100g(), 0.0) / 100.0;
            case FIBER -> valueOrDefault(food.getFiberPer100g(), 0.0) / 100.0;
            case COST -> valueOrDefault(food.getCostPer100g(), 0.0) / 100.0;
        };
    }

    private DietOptimizationResult buildResult(
            MPVariable[] variables,
            List<FoodItem> foods
    ) {
        double totalCalories = 0.0;
        double totalProtein = 0.0;
        double totalCarbs = 0.0;
        double totalFat = 0.0;
        double totalFiber = 0.0;
        double totalCost = 0.0;

        List<OptimizedFoodItem> resultItems = new ArrayList<>();

        for (int i = 0; i < foods.size(); i++) {
            FoodItem food = foods.get(i);
            double quantity = variables[i].solutionValue();

            if (quantity > 0.01) {
                resultItems.add(
                        new OptimizedFoodItem(
                                food.getId(),
                                food.getName(),
                                round2(quantity),
                                "g/ml"
                        )
                );

                totalCalories += quantity * valueOrDefault(food.getCaloriesPer100g(), 0.0) / 100.0;
                totalProtein += quantity * valueOrDefault(food.getProteinPer100g(), 0.0) / 100.0;
                totalCarbs += quantity * valueOrDefault(food.getCarbsPer100g(), 0.0) / 100.0;
                totalFat += quantity * valueOrDefault(food.getFatPer100g(), 0.0) / 100.0;
                totalFiber += quantity * valueOrDefault(food.getFiberPer100g(), 0.0) / 100.0;
                totalCost += quantity * valueOrDefault(food.getCostPer100g(), 0.0) / 100.0;
            }
        }

        return new DietOptimizationResult(
                "OPTIMAL",
                round2(totalCalories),
                round2(totalProtein),
                round2(totalCarbs),
                round2(totalFat),
                round2(totalFiber),
                round2(totalCost),
                resultItems
        );
    }

    private DietOptimizationResult emptyResult(String status) {
        return new DietOptimizationResult(
                status,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                List.of()
        );
    }

    private double valueOrDefault(Double value, double defaultValue) {
        return value == null ? defaultValue : value;
    }

    private double valueOrInfinity(Double value) {
        return value == null ? Double.POSITIVE_INFINITY : value;
    }

    private double round2(double value) {
        return Math.round(value * 100.0) / 100.0;
    }

    private String safeVariableName(String name) {
        if (name == null || name.isBlank()) {
            return "food";
        }

        return name.replaceAll("[^a-zA-Z0-9_]", "_");
    }

    private enum NutrientType {
        CALORIES,
        PROTEIN,
        CARBS,
        FAT,
        FIBER,
        COST
    }
}