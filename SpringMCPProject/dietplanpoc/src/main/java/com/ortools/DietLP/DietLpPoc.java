package com.ortools.DietLP;

import com.google.ortools.Loader;
import com.google.ortools.linearsolver.MPConstraint;
import com.google.ortools.linearsolver.MPObjective;
import com.google.ortools.linearsolver.MPSolver;
import com.google.ortools.linearsolver.MPVariable;

import java.util.ArrayList;
import java.util.List;

public class DietLpPoc {

    static class Food {
        String name;

        // Nutrition per 100g or 100ml
        double caloriesPer100g;
        double proteinPer100g;
        double carbsPer100g;
        double fatPer100g;
        double fiberPer100g;

        // Cost per 100g or 100ml
        double costPer100g;

        // Daily min/max quantity
        double minGrams;
        double maxGrams;

        Food(
                String name,
                double caloriesPer100g,
                double proteinPer100g,
                double carbsPer100g,
                double fatPer100g,
                double fiberPer100g,
                double costPer100g,
                double minGrams,
                double maxGrams
        ) {
            this.name = name;
            this.caloriesPer100g = caloriesPer100g;
            this.proteinPer100g = proteinPer100g;
            this.carbsPer100g = carbsPer100g;
            this.fatPer100g = fatPer100g;
            this.fiberPer100g = fiberPer100g;
            this.costPer100g = costPer100g;
            this.minGrams = minGrams;
            this.maxGrams = maxGrams;
        }
    }

    public static void main(String[] args) {
        Loader.loadNativeLibraries();

        /*
         * GLOP = Google's Linear Optimization Package.
         * Use GLOP for pure Linear Programming.
         */
        MPSolver solver = MPSolver.createSolver("GLOP");

        if (solver == null) {
            System.out.println("Could not create solver.");
            return;
        }

        /*
         * For POC, food data is hardcoded.
         * Later, this will come from OpenNutrition / USDA / database.
         */
        List<Food> foods = List.of(
                new Food("Oats",          389, 16.9, 66.3,  6.9, 10.6, 0.35, 0,   150),
                new Food("Milk",           61,  3.2,  4.8,  3.3,  0.0, 0.18, 0,   750),
                new Food("Banana",         89,  1.1, 22.8,  0.3,  2.6, 0.30, 0,   300),
                new Food("Eggs",          143, 12.6,  0.7,  9.5,  0.0, 0.60, 0,   150),
                new Food("Rice cooked",   130,  2.7, 28.0,  0.3,  0.4, 0.20, 0,   600),
                new Food("Ground beef",   250, 26.0,  0.0, 15.0,  0.0, 1.20, 0,   300),
                new Food("Pasta cooked",  158,  5.8, 30.9,  0.9,  1.8, 0.25, 0,   600),
                new Food("Peanut butter", 588, 25.0, 20.0, 50.0,  6.0, 0.90, 0,    40),
                new Food("Vegetables",     50,  2.0, 10.0,  0.5,  4.0, 0.40, 200, 700)
        );

        int n = foods.size();

        /*
         * Decision variable:
         * x[i] = grams/ml of food i per day
         */
        MPVariable[] x = new MPVariable[n];

        for (int i = 0; i < n; i++) {
            Food food = foods.get(i);

            x[i] = solver.makeNumVar(
                    food.minGrams,
                    food.maxGrams,
                    food.name
            );
        }

        /*
         * Daily constraints.
         *
         * 2900 <= calories <= 3100
         * protein >= 130g
         * 350 <= carbs <= 430
         * 70 <= fat <= 95
         * fiber >= 30g
         * cost <= $15
         */

        addConstraint(solver, x, foods, 2900, 3100, "calories", "calories");
        addConstraint(solver, x, foods, 130, Double.POSITIVE_INFINITY, "protein", "protein");
        addConstraint(solver, x, foods, 350, 430, "carbs", "carbs");
        addConstraint(solver, x, foods, 70, 95, "fat", "fat");
        addConstraint(solver, x, foods, 30, Double.POSITIVE_INFINITY, "fiber", "fiber");
        addConstraint(solver, x, foods, 0, 15, "budget", "cost");

        /*
         * Objective:
         * Minimize total food cost.
         */
        MPObjective objective = solver.objective();

        for (int i = 0; i < n; i++) {
            Food food = foods.get(i);

            double costPerGram = food.costPer100g / 100.0;
            objective.setCoefficient(x[i], costPerGram);
        }

        objective.setMinimization();

        /*
         * Solve the LP.
         */
        MPSolver.ResultStatus status = solver.solve();

        if (status != MPSolver.ResultStatus.OPTIMAL) {
            System.out.println("No optimal solution found.");
            System.out.println("Solver status: " + status);
            return;
        }

        /*
         * Print result.
         */
        double totalCalories = 0;
        double totalProtein = 0;
        double totalCarbs = 0;
        double totalFat = 0;
        double totalFiber = 0;
        double totalCost = 0;

        List<String> selectedFoods = new ArrayList<>();

        System.out.println("Optimal Daily Diet Plan");
        System.out.println("=======================");

        for (int i = 0; i < n; i++) {
            double quantity = x[i].solutionValue();

            if (quantity > 0.01) {
                Food food = foods.get(i);

                selectedFoods.add(food.name);

                double calories = quantity * food.caloriesPer100g / 100.0;
                double protein = quantity * food.proteinPer100g / 100.0;
                double carbs = quantity * food.carbsPer100g / 100.0;
                double fat = quantity * food.fatPer100g / 100.0;
                double fiber = quantity * food.fiberPer100g / 100.0;
                double cost = quantity * food.costPer100g / 100.0;

                totalCalories += calories;
                totalProtein += protein;
                totalCarbs += carbs;
                totalFat += fat;
                totalFiber += fiber;
                totalCost += cost;

                System.out.printf(
                        "%-15s %8.2f g/ml   Cost: $%.2f%n",
                        food.name,
                        quantity,
                        cost
                );
            }
        }

        System.out.println();
        System.out.println("Totals");
        System.out.println("======");
        System.out.printf("Calories: %.2f kcal%n", totalCalories);
        System.out.printf("Protein:  %.2f g%n", totalProtein);
        System.out.printf("Carbs:    %.2f g%n", totalCarbs);
        System.out.printf("Fat:      %.2f g%n", totalFat);
        System.out.printf("Fiber:    %.2f g%n", totalFiber);
        System.out.printf("Cost:     $%.2f per day%n", totalCost);

        System.out.println();
        System.out.println("Solver Info");
        System.out.println("===========");
        System.out.println("Status: " + status);
        System.out.println("Variables: " + solver.numVariables());
        System.out.println("Constraints: " + solver.numConstraints());
        System.out.println("Objective value: " + objective.value());
    }

    private static void addConstraint(
            MPSolver solver,
            MPVariable[] variables,
            List<Food> foods,
            double lowerBound,
            double upperBound,
            String constraintName,
            String nutrientType
    ) {
        MPConstraint constraint = solver.makeConstraint(
                lowerBound,
                upperBound,
                constraintName
        );

        for (int i = 0; i < foods.size(); i++) {
            Food food = foods.get(i);

            double coefficient = switch (nutrientType) {
                case "calories" -> food.caloriesPer100g / 100.0;
                case "protein" -> food.proteinPer100g / 100.0;
                case "carbs" -> food.carbsPer100g / 100.0;
                case "fat" -> food.fatPer100g / 100.0;
                case "fiber" -> food.fiberPer100g / 100.0;
                case "cost" -> food.costPer100g / 100.0;
                default -> throw new IllegalArgumentException("Unknown nutrient type: " + nutrientType);
            };

            constraint.setCoefficient(variables[i], coefficient);
        }
    }
}

/* Output
Optimal Daily Diet Plan
=======================
Oats              150.00 g/ml   Cost: $0.53
Milk              259.15 g/ml   Cost: $0.47
Eggs              150.00 g/ml   Cost: $0.90
Rice cooked       370.22 g/ml   Cost: $0.74
Ground beef        71.77 g/ml   Cost: $0.86
Pasta cooked      600.00 g/ml   Cost: $1.50
Peanut butter      40.00 g/ml   Cost: $0.36
Vegetables        200.00 g/ml   Cost: $0.80

Totals
======
Calories: 2900.00 kcal
Protein:  130.00 g
Carbs:    430.00 g
Fat:      71.43 g
Fiber:    38.58 g
Cost:     $6.15 per day

Solver Info
===========
Status: OPTIMAL
Variables: 9
Constraints: 6
Objective value: 6.153197207446809
*/