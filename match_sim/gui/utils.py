
import wx

def ptable_to_grid(parent, atable):
  x = wx.grid.Grid(parent)
  rows = atable._rows
  cols = atable._field_names
  x.CreateGrid(min(15, len(rows)), len(cols))
  i = 0
  j = 0
  G = "\033[0;32;40m" # Green
  N = "\033[0m" # Reset
  for col in cols:
    x.SetColLabelValue(j, str(col))
    j += 1
  i = 0
  for arow in rows:
    j = 0
    if i < 15:
      for acol in arow:
        x.SetCellValue(i, j, str(acol).replace(G, '').replace(N, ''))
        x.SetReadOnly(i, j)
        j += 1
    i += 1
  x.HideRowLabels()
  return x
