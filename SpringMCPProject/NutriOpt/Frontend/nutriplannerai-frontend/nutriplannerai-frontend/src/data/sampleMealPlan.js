export const sampleMealPlan = {
  totals: {
    calories: 2810,
    protein: 123,
    carbs: 365,
    fat: 82,
    fiber: 31
  },
  targets: {
    calories: 2800,
    protein: 120,
    carbs: 400,
    fat: 90,
    fiber: 25
  },
  cost: {
    total: 13.8,
    estimated: true
  },
  badges: [
    { label: 'RELAXED OPTIMIZATION', type: 'warning' },
    { label: 'PRICE ESTIMATED', type: 'info' }
  ],
  macroDistribution: {
    carbs: 52,
    protein: 18,
    fat: 30
  },
  optimization: {
    badges: [
      { label: 'INFEASIBLE FIRST', type: 'warning' },
      { label: 'OPTIMAL FINAL', type: 'success' }
    ],
    note: 'The first LP attempt was infeasible, so the agent relaxed the fat range slightly and added more vegetarian food options.'
  },
  meals: [
    {
      name: 'Breakfast',
      icon: '🌅',
      description: 'High-energy start',
      calories: 720,
      protein: 32,
      cost: 2.45,
      items: [
        { food: 'Oats', quantity: '90g' },
        { food: 'Milk', quantity: '300ml' },
        { food: 'Banana', quantity: '1 medium' },
        { food: 'Peanut butter', quantity: '20g' }
      ]
    },
    {
      name: 'Lunch',
      icon: '☀️',
      description: 'Protein and fiber focused',
      calories: 1040,
      protein: 48,
      cost: 5.35,
      items: [
        { food: 'Rice', quantity: '260g cooked' },
        { food: 'Lentils', quantity: '220g cooked' },
        { food: 'Greek yogurt', quantity: '170g' },
        { food: 'Vegetables', quantity: '180g' }
      ]
    },
    {
      name: 'Dinner',
      icon: '🌙',
      description: 'Balanced evening meal',
      calories: 1050,
      protein: 43,
      cost: 6.0,
      items: [
        { food: 'Pasta', quantity: '240g cooked' },
        { food: 'Tofu', quantity: '200g' },
        { food: 'Chickpeas', quantity: '120g' },
        { food: 'Vegetables', quantity: '200g' }
      ]
    }
  ]
};
