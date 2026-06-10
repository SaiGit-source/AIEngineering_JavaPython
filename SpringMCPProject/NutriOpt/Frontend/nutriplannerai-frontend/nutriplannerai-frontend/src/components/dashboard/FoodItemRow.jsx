export default function FoodItemRow({ item }) {
  return (
    <div className="food-item-row">
      <span>{item.food}</span>
      <strong>{item.quantity}</strong>
    </div>
  );
}
