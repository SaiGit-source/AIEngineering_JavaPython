package com.nutriopt.MCPServer.tools;

import com.nutriopt.MCPServer.dto.DietOptimizationRequest;
import com.nutriopt.MCPServer.dto.DietOptimizationResult;
import com.nutriopt.MCPServer.model.FoodItem;
import com.nutriopt.MCPServer.repo.FoodItemRepo;
import com.nutriopt.MCPServer.service.LpSolverService;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class LpOptimizerTool {

    private final FoodItemRepo foodItemRepository;
    private final LpSolverService lpSolverService;

    public LpOptimizerTool(
            FoodItemRepo foodItemRepository,
            LpSolverService lpSolverService
    ) {
        this.foodItemRepository = foodItemRepository;
        this.lpSolverService = lpSolverService;
    }

    @Tool(description = "Optimize a one-day diet using Linear Programming. Reads selected foods from MariaDB by food IDs and minimizes daily cost while satisfying macro constraints.")
    public DietOptimizationResult optimizeDietLp(DietOptimizationRequest request) {

        if (request == null || request.foodIds() == null || request.foodIds().isEmpty()) {
            return new DietOptimizationResult(
                    "NO_FOOD_IDS_PROVIDED",
                    0, 0, 0, 0, 0, 0,
                    List.of()
            );
        }

        List<FoodItem> foods = foodItemRepository.findAllById(request.foodIds());

        if (foods.isEmpty()) {
            return new DietOptimizationResult(
                    "NO_FOODS_FOUND_IN_DATABASE",
                    0, 0, 0, 0, 0, 0,
                    List.of()
            );
        }

        return lpSolverService.solve(request.targets(), foods);
    }
}