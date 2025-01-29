import React, { useState, Children, cloneElement } from 'react';

interface TabsProps {
  defaultValue: string;
  className?: string;
  onValueChange?: (value: string) => void;
  children: React.ReactNode;
}

const Tabs = React.forwardRef<HTMLDivElement, TabsProps>(({ defaultValue, className, onValueChange, children }, ref) => {
  const [value, setValue] = useState(defaultValue);

  const handleValueChange = (newValue: string) => {
    setValue(newValue);
    if (onValueChange) {
      onValueChange(newValue);
    }
  };

  return (
    <div className={`tabs ${className}`} ref={ref}>
      {Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          return cloneElement(child, { value: value, currentValue: value, onValueChange: handleValueChange } as any);
        }
        return child;
      })}
    </div>
  );
});

Tabs.displayName = "Tabs";

interface TabsListProps {
  className?: string;
  children: React.ReactNode;
}

const TabsList = React.forwardRef<HTMLDivElement, TabsListProps>(({ className, children }, ref) => {
  return (
    <div className={`tabs-list ${className}`} role="tablist" ref={ref}>
      {children}
    </div>
  );
});

TabsList.displayName = "TabsList";


interface TabsTabProps {
  value: string;
  className?: string;
  children: React.ReactNode;
  onValueChange: (value: string) => void;
  currentValue?: string;
}

const TabsTab = React.forwardRef<HTMLButtonElement, TabsTabProps>(({ value, className, children, onValueChange, currentValue }, ref) => {
  const isActive = currentValue === value;

  return (
    <button
      ref={ref}
      className={`tabs-tab ${className} ${isActive ? 'active' : ''}`}
      role="tab"
      aria-selected={isActive}
      aria-controls={`${value}-panel`}
      id={value}
      onClick={() => onValueChange(value)}
    >
      {children}
    </button>
  );
});

TabsTab.displayName = "TabsTab";


interface TabsPanelProps {
  value: string;
  className?: string;
  children: React.ReactNode;
  currentValue?: string;
}

const TabsPanel = React.forwardRef<HTMLDivElement, TabsPanelProps>(({ value, className, children, currentValue }, ref) => {
  const isActive = currentValue === value;

  return (
    <div
      ref={ref}
      className={`tabs-panel ${className} ${isActive ? 'active' : 'hidden'}`}
      role="tabpanel"
      aria-labelledby={value}
      id={`${value}-panel`}
    >
      {children}
    </div>
  );
});

TabsPanel.displayName = "TabsPanel";


export { Tabs, TabsList, TabsTab, TabsPanel };