interface StrategySelectProps {
  onStrategyChange: (strategy: string) => void;
}

export const StrategySelect: React.FC<StrategySelectProps> = ({ onStrategyChange }) => {
  return (
    <select onChange={(e) => onStrategyChange(e.target.value)} defaultValue="liquidations_schaff_trend_cycle_p1">
      <option value="liquidations_schaff_trend_cycle_p1">Liquidations & STC</option>
    </select>
  );
}; 