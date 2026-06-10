export function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return '0';
  }

  return new Intl.NumberFormat('en-CA', {
    maximumFractionDigits: 1
  }).format(value);
}

export function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return '$0.00';
  }

  return new Intl.NumberFormat('en-CA', {
    style: 'currency',
    currency: 'CAD'
  }).format(value);
}
