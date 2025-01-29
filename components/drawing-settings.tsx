"use client";

import React, { useState } from "react";
import { Input } from "components/ui/input";

interface DrawingSettingsProps {
  onSettingsChange: (settings: DrawingSettings) => void;
}

interface DrawingSettings {
    lineThickness: number;
    color: string;
    backgroundColor: string;
    transparency: number;
}

export function DrawingSettings({ onSettingsChange }: DrawingSettingsProps) {
  const [lineThickness, setLineThickness] = useState<number>(1);
  const [color, setColor] = useState<string>("#000000");
  const [backgroundColor, setBackgroundColor] = useState<string>("#ffffff");
  const [transparency, setTransparency] = useState<number>(1);

  const handleLineThicknessChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    setLineThickness(value);
    onSettingsChange({ lineThickness: value, color, backgroundColor, transparency });
  };

  const handleColorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setColor(value);
    onSettingsChange({ lineThickness, color: value, backgroundColor, transparency });
  };

    const handleBackgroundColorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setBackgroundColor(value);
    onSettingsChange({ lineThickness, color, backgroundColor: value, transparency });
  };

  const handleTransparencyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(e.target.value);
      setTransparency(value);
    onSettingsChange({ lineThickness, color, backgroundColor, transparency: value });
  };


  return (
    <div className="flex flex-col space-y-2 p-2">
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Line Thickness
        </label>
        <Input
          type="number"
          value={lineThickness}
          onChange={handleLineThicknessChange}
          className="mt-1"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Color
        </label>
         <Input
          type="color"
          value={color}
          onChange={handleColorChange}
          className="mt-1"
        />
      </div>
        <div>
        <label className="block text-sm font-medium text-gray-700">
          Background Color
        </label>
         <Input
          type="color"
          value={backgroundColor}
          onChange={handleBackgroundColorChange}
          className="mt-1"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Transparency
        </label>
        <Input
          type="number"
          value={transparency}
          onChange={handleTransparencyChange}
          step="0.1"
          min="0"
          max="1"
          className="mt-1"
        />
      </div>
    </div>
  );
}