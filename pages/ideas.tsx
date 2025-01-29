import React from 'react';
import { Sidebar } from '../components/sidebar';

const mockStock = {
	symbol: "AAPL",
	price: 150.23,
	change: 2.5,
	changePercent: 1.67,
	companyName: "Apple Inc.",
	exchange: "NASDAQ",
	industry: "Technology",
	lastUpdated: "2024-01-19 16:00:00",
	// ... add other required fields with default values
};

export default function IdeasPage() {
	return (
		<div className="flex h-screen bg-[#1a1a1a]">
			<div className="flex-1">
				{/* Content area without chart and top panel */}
			</div>
			<div className="w-[350px]">
				<Sidebar currentStock={mockStock} />
			</div>
		</div>
	);
}