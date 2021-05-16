
import wx

def ptable_to_grid(parent, atable, keep_cols=None, subset_rows=None, sort_col=None):
  x = wx.grid.Grid(parent)
  x.DisableDragGridSize()
  x.DisableCellEditControl()
  rows = atable._rows
  cols = atable._field_names
  x.CreateGrid(len(rows), len(cols))
  j = 0
  G = "\033[0;32;40m" # Green
  N = "\033[0m" # Reset
  for col in cols:
    x.SetColLabelValue(j, str(col))
    j += 1
  i = 0
  for arow in rows:
    j = 0
    for acol in arow:
      tname = 'str'
      if isinstance(acol, float):
        x.SetColFormatFloat(j)
        acol = round(acol, 2)
        # print(aval)
      elif isinstance(acol, int):
        x.SetColFormatNumber(j)
      aval = str(acol).replace(G, '').replace(N, '')
      x.SetCellValue(i, j, aval)
      x.SetReadOnly(i, j)
      j += 1
    i += 1
  x.HideRowLabels()
  if keep_cols is None:
    keep_cols = cols[:]
  i = 0
  for col in cols:
    if col not in keep_cols:
      x.DeleteCols(i, 1)
      i -= 1
    else:
      x.DisableColResize(i)
      # x.DisableRowResize()
    i += 1
  if subset_rows is not None:
    keep_row = subset_rows.split(' ')[0]
    keep_row_j = cols.index(keep_row)
    condition = subset_rows.split (' ')[1]
    val = float(subset_rows.split(' ')[2])
    i = 0
    for arow in rows:
      j = 0
      for acol in arow:
        if j == keep_row_j:
          if condition == '<':
            if (acol < val) is False:
              x.DeleteRows(i, 1)
              i -= 1
          elif condition == '>':
            if (acol > val) is False:
              x.DeleteRows(i, 1)
              i -= 1
        j += 1
      i += 1
  if sort_col is not None:
    if sort_col in keep_cols:
      x.UnsetSortingColumn()
      x.SetSortingColumn(keep_cols.index(sort_col))
  x.AutoSize()
  # x.SetMargins(0, 0)
  return x
