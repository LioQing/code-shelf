import React from 'react';

interface TableProps extends React.HTMLProps<HTMLTableElement> {
  values: React.ReactNode[][];
  columnHeaders?: React.ReactNode[];
  rowHeaders?: React.ReactNode[];
}

const TableHeader = ({ values }: { values: React.ReactNode[] }) => {
  return (
    <thead>
      <tr>
        {values.map((value, index) => (
          <th key={index}>{value}</th>
        ))}
      </tr>
    </thead>
  );
}

const TableBody = ({ values, rowHeaders }: { values: React.ReactNode[][], rowHeaders?: React.ReactNode[] }) => {
  return (
    <tbody>
      {values.map((row, rowIndex) => (
        <tr key={rowIndex}>
          {rowHeaders && <th>{rowHeaders[rowIndex]}</th>}
          {row.map((value, colIndex) => (
            <td key={colIndex}>{value}</td>
          ))}
        </tr>
      ))}
    </tbody>
  );
}

const Table = ({ values, columnHeaders, rowHeaders }: TableProps) => {
  // Props validation
  const colCount = columnHeaders ? columnHeaders.length : values[0].length;
  if (values.some(row => row.length !== colCount)) {
    throw new Error('All rows must have the same number of columns');
  }

  const rowCount = rowHeaders ? rowHeaders.length : values.length;
  if (values.length !== rowCount) {
    throw new Error('All rows must have the same number of columns');
  }

  // Render
  return (
    <table>
      {columnHeaders && <TableHeader values={columnHeaders} />}
      <TableBody values={values} rowHeaders={rowHeaders} />
    </table>
  );
}

export default Table;