import { sampleMealPlan } from '../data/sampleMealPlan.js';

export function parseMealPlanFromText(aiText) {
  if (!aiText || typeof aiText !== 'string') {
    return sampleMealPlan;
  }

  // First version fallback: keep dashboard stable with sample structure.
  // Later, replace this with strict parsing or a backend JSON response.
  return sampleMealPlan;
}
