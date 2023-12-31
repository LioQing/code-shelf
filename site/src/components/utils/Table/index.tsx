import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface TableProps extends React.HTMLProps<HTMLTableElement> {
  values: React.ReactNode[][];
  columnHeaders?: React.ReactNode[];
  rowHeaders?: React.ReactNode[];
}

const TableHeader = ({ hasRow, values }: { hasRow: boolean, values: React.ReactNode[] }) => {
  return (
    <thead>
      <tr>
        {(hasRow ? ['' as React.ReactNode] : []).concat(values).map((value, index) => (
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

const Table = ({ values, columnHeaders, rowHeaders, className, ...tableProps }: TableProps) => {
  // Props validation
  const colCount = columnHeaders ? columnHeaders.length : values[0].length;
  if (values.some(row => row.length !== colCount)) {
    const index = values.findIndex(row => row.length !== colCount);
    const wrongColCount = values[index].length;
    throw new Error(`
      All rows must have the same number of columns:
      row ${columnHeaders ? 'header' : '0'} has ${colCount}, row ${index} has ${wrongColCount} columns
    `);
  }

  const rowCount = rowHeaders ? rowHeaders.length : values.length;
  if (values.length !== rowCount) {
    throw new Error(`
      The number of row headers must match the number of rows:
      ${rowCount} row headers, ${values.length} rows
    `);
  }

  const classNames = className ? clsx(styles.table, className) : styles.table;

  // Render
  return (
    <div className={styles.scroller}>
      <table className={classNames} {...tableProps}>
        {columnHeaders
          && <TableHeader hasRow={rowHeaders !== undefined} values={columnHeaders} />
        }
        <TableBody values={values} rowHeaders={rowHeaders} />
      </table>
    </div>
  );
}

export default Table;