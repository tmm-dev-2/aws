"use client"
import { Card } from "@/dashboard-components/ui/card"
import type { ColumnDef } from "@tanstack/react-table"
import { Table, TableBody, TableCell, TableHeader, TableRow } from "dashboard/components/ui/table"
import type { StockMover, StockMoversData } from "@/types/stock-movers"
import { Badge } from "dashboard/components/ui/badge"
import { formatNumber } from "@/lib/format-number"
import { useState, useEffect } from "react"

interface StockMoversProps {
  data: StockMoversData
}

const columns: ColumnDef<StockMover>[] = [
  {
    accessorKey: "symbol",
    header: "Symbol",
  },
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "price",
    header: "Price",
    cell: ({ row }) => <span>${formatNumber(row.getValue("price"))}</span>,
  },
  {
    accessorKey: "change",
    header: "Change",
    cell: ({ row }) => (
      <Badge variant={row.getValue("change") > 0 ? "success" : "danger"}>{formatNumber(row.getValue("change"))}%</Badge>
    ),
  },
  {
    accessorKey: "volume",
    header: "Volume",
    cell: ({ row }) => <span>{formatNumber(row.getValue("volume"))}</span>,
  },
]

export function StockMovers({ data }: StockMoversProps) {
  const [stockMovers, setStockMovers] = useState<StockMover[]>([])

  useEffect(() => {
    setStockMovers(data.stockMovers)
  }, [data])

  return (
    <Card className="col-span-12 lg:col-span-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-medium">Stock Movers</h2>
      </div>
      <Table>
        <TableHeader>
          {columns.map((column) => (
            <th key={column.accessorKey} className="p-4">
              {column.header}
            </th>
          ))}
        </TableHeader>
        <TableBody>
          {stockMovers.map((stockMover) => (
            <TableRow key={stockMover.symbol}>
              {columns.map((column) => (
                <TableCell key={column.accessorKey}>
                  {column.cell
                    ? column.cell({ row: { getValue: (key) => stockMover[key] } })
                    : stockMover[column.accessorKey]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Card>
  )
}

