export default function PromptInput({ value, onChange, onSubmit, disabled }) {
  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="prompt-input-card">
      <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Example: Create a vegetarian 2800 calorie meal plan with breakfast, lunch and dinner..."
        rows={4}
        disabled={disabled}
      />
      <button type="button" onClick={onSubmit} disabled={disabled || !value.trim()}>
        {disabled ? 'Planning...' : 'Send Prompt'}
      </button>
    </div>
  );
}
