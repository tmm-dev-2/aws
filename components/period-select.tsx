interface PeriodSelectProps {
  onPeriodChange: (period: string) => void;
}

export const PeriodSelect: React.FC<PeriodSelectProps> = ({ onPeriodChange }) => {
  return (
    <select onChange={(e) => onPeriodChange(e.target.value)} defaultValue="1d">
      {/* Daily timeframes */}
      <optgroup label="Daily">
        <option value="1d">1 Day</option>
        <option value="2d">2 Days</option>
      </optgroup>

      {/* Weekly timeframes */}
      <optgroup label="Weekly">
        <option value="1w">1 Week</option>
        <option value="2w">2 Weeks</option>
      </optgroup>

      {/* Monthly timeframes */}
      <optgroup label="Monthly">
        <option value="1m">1 Month</option>
        <option value="2m">2 Months</option>
        <option value="3m">3 Months</option>
        <option value="6m">6 Months</option>
      </optgroup>

      {/* Yearly */}
      <optgroup label="Yearly">
        <option value="1y">1 Year</option>
      </optgroup>
    </select>
  );
}; 