/*
 * The main part of the `HeatMap` component, which renders the row labels and all of the matrix
 * cells.  Each row is a div, and each cell is an inline div inside of that, with a background
 * color determined by the data value.
 */
import React from 'react';

const DataGrid = ({
  xLabels,
  yLabels,
  data,
  xLabelWidth,
  boxSize,
  background,
  height,
}) => {
  const flatArray = data.reduce((i, o) => [...o, ...i], []);
  const max = Math.max(...flatArray);
  const min = Math.min(...flatArray);
  return (
    <div style={{"white-space": "nowrap"}}>
      {yLabels.map((y, yi) => (
        <div key={`${y}_${yi}`} style={{clear: "both"}}>
          {xLabels.map((x, xi) => (
            <div
              title={`${data[yi][xi]}`}
              key={`${x}_${xi}_${y}_${yi}`}
              style={{
                background,
                display: "inline-block",
                margin: '1px 1px 0 0',
                width: boxSize,
                height: boxSize,
                opacity: (data[yi][xi] - min) / (max - min),
              }}
            >
            &nbsp;
            </div>
          ))}
          <div style={{display: "inline-block", width: xLabelWidth, textAlign: 'right', paddingLeft: `${boxSize+5}px`}}>{y}</div>
        </div>
      ))}
    </div>
  );
};

export default DataGrid;
