import React from 'react';
import { Listbox } from '@headlessui/react';

interface MultiSelectProps {
  options: string[];
  value: string[];
  onChange: (value: string[]) => void;
  placeholder: string;
}

export function MultiSelect({ options, value, onChange, placeholder }: MultiSelectProps) {
  return (
    <Listbox value={value} onChange={onChange} multiple>
      <div className="relative">
        <Listbox.Button className="w-full bg-[#1a1a1a] text-white p-2 rounded text-left">
          {value.length > 0 ? value.join(', ') : placeholder}
        </Listbox.Button>
        <Listbox.Options className="absolute z-10 w-full mt-1 bg-[#242424] rounded shadow-lg max-h-60 overflow-auto">
          {options.map((option) => (
            <Listbox.Option
              key={option}
              value={option}
              className={({ active, selected }) =>
                `p-2 cursor-pointer ${active ? 'bg-blue-500' : ''} ${
                  selected ? 'bg-blue-700' : ''
                }`
              }
            >
              {option}
            </Listbox.Option>
          ))}
        </Listbox.Options>
      </div>
    </Listbox>
  );
}