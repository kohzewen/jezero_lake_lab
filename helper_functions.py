import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from shapely.geometry import LineString, Polygon
from matplotlib.colors import LightSource
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import PolygonSelector

def is_interactive():
    """True if figures are interactive (ipympl 'widget' backend)."""
    backend = matplotlib.get_backend().lower()
    return "ipympl" in backend or "widget" in backend


def da_extent(da):
    """(left, right, bottom, top) of a 2-D DataArray, for plt.imshow(extent=...)."""
    x, y = da.x.values, da.y.values
    dx, dy = abs(x[1] - x[0]), abs(y[1] - y[0])
    return (x.min() - dx / 2, x.max() + dx / 2, y.min() - dy / 2, y.max() + dy / 2)


def hillshade(da, azdeg=315, altdeg=35, vert_exag=2.0):
    """Shaded-relief image (0-1) of a DEM DataArray."""
    dx, dy = abs(float(da.x[1] - da.x[0])), abs(float(da.y[1] - da.y[0]))
    z = da.values.astype(float)
    z = np.where(np.isnan(z), np.nanmean(z), z)
    return LightSource(azdeg=azdeg, altdeg=altdeg).hillshade(z, vert_exag=vert_exag, dx=dx, dy=dy)


def km_axes(ax, label=True):
    """Label projected axes (metres) in km."""
    fmt = FuncFormatter(lambda v, pos: f"{v / 1e3:.0f}")
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_major_formatter(fmt)
    if label:
        ax.set_xlabel("x (km)")
        ax.set_ylabel("y (km)")


def plot_basemap(ax, da, step=4, extent=None, cmap="terrain", alpha=0.45, colorbar=True, **kwargs):
    """Hillshade + semi-transparent elevation colours.

    step   : plot every `step`-th pixel (faster for big rasters)
    extent : (xmin, xmax, ymin, ymax) in map units, to zoom in
    """
    if extent is not None:
        xmin, xmax, ymin, ymax = extent
        da = da.sel(x=slice(xmin, xmax), y=slice(ymax, ymin))
    sub = da[::step, ::step]
    ext = da_extent(sub)
    ax.imshow(hillshade(sub), cmap="gray", extent=ext, interpolation="nearest")
    im = ax.imshow(sub.values, cmap=cmap, alpha=alpha, extent=ext, interpolation="nearest", **kwargs)
    if colorbar:
        plt.colorbar(im, ax=ax, label="Elevation (m)", shrink=0.8)
    ax.set_aspect("equal")
    return im


def profile_along(da, points, spacing=None, swath_halfwidth=0.0):
    """Sample a DEM along a polyline.

    points          : list of (x, y) vertices in the DEM's CRS
    spacing         : distance between samples (default: one pixel)
    swath_halfwidth : if > 0, at every sample take the MINIMUM elevation within
                      +/- this distance perpendicular to the line. Useful for
                      following a valley floor when your line is slightly off-centre.
    Returns (distance, elevation, x, y) as numpy arrays (distance in metres).
    """
    res = abs(da.rio.resolution()[0])
    spacing = spacing or res
    line = LineString(points)
    dist = np.append(np.arange(0, line.length, spacing), line.length)
    xy = np.array([line.interpolate(d).coords[0] for d in dist])
    xs, ys = xy[:, 0], xy[:, 1]
    if swath_halfwidth > 0:
        tx, ty = np.gradient(xs), np.gradient(ys)
        norm = np.hypot(tx, ty)
        norm[norm == 0] = 1
        nx, ny = -ty / norm, tx / norm
        offsets = np.arange(-swath_halfwidth, swath_halfwidth + res / 2, res)
        X = xs[:, None] + offsets[None, :] * nx[:, None]
        Y = ys[:, None] + offsets[None, :] * ny[:, None]
    else:
        X, Y = xs[:, None], ys[:, None]
    z = da.sel(x=xr.DataArray(X, dims=("s", "o")), y=xr.DataArray(Y, dims=("s", "o")),
               method="nearest").values
    return dist, np.nanmin(z, axis=1), xs, ys


class LineDrawer:
    """Interactive elevation-profile tool.

    * Left-click on the map to add points; the profile (right) updates after each click.
    * Keyboard (click the figure first): 'u' = undo last point, 'c' = clear all points.
    * To zoom, use the toolbar's zoom/pan buttons -- then switch them OFF before clicking points.
    * `.get_profile()` returns (distance_m, elevation_m) along your line.
    * `outline` (optional): a GeoDataFrame/GeoSeries of polygons (e.g. the lake) whose
      boundary is drawn on the map for reference.
    """

    def __init__(self, da, title="Click to draw a line", extent=None, step=4,
                 swath_halfwidth=0.0, ref_levels=None, color="red", figsize=(10.5, 4.6),
                 width_ratios=(1, 1.25), outline=None):
        self.da = da
        self.swath_halfwidth, self.ref_levels, self.color = swath_halfwidth, ref_levels or {}, color
        self.points = []
        self.fig, (self.ax_map, self.ax_prof) = plt.subplots(
            1, 2, figsize=figsize, gridspec_kw={"width_ratios": list(width_ratios)})
        plot_basemap(self.ax_map, da, step=step, extent=extent, colorbar=False)
        if outline is not None:
            xlim, ylim = self.ax_map.get_xlim(), self.ax_map.get_ylim()
            outline.boundary.plot(ax=self.ax_map, color="navy", lw=1.2)
            self.ax_map.set_xlim(xlim)       # keep the zoom of the map
            self.ax_map.set_ylim(ylim)
        km_axes(self.ax_map)
        self.ax_map.set_title(title, fontsize=10)
        (self.map_line,) = self.ax_map.plot([], [], ".-", color=color, lw=1.5, ms=6)
        (self.start_marker,) = self.ax_map.plot([], [], "o", mfc="none", mec=color, ms=11, mew=2)
        self.fig.canvas.mpl_connect("button_press_event", self._on_click)
        self.fig.canvas.mpl_connect("key_press_event", self._on_key)
        self._update()
        self.fig.tight_layout()

    def set_points(self, points):
        self.points = [tuple(p) for p in points]
        self._update()

    def _on_click(self, event):
        if event.inaxes is not self.ax_map or event.button != 1:
            return
        toolbar = getattr(self.fig.canvas, "toolbar", None)
        if toolbar is not None and getattr(toolbar, "mode", "") != "":
            return  # zoom/pan is active
        self.points.append((event.xdata, event.ydata))
        self._update()

    def _on_key(self, event):
        if event.key == "u" and self.points:
            self.points.pop()
        elif event.key == "c":
            self.points = []
        self._update()

    def _update(self):
        pts = np.array(self.points) if self.points else np.empty((0, 2))
        self.map_line.set_data(pts[:, 0], pts[:, 1])
        self.start_marker.set_data(pts[:1, 0], pts[:1, 1])
        ax = self.ax_prof
        ax.cla()
        ax.set_xlabel("Distance from start of line (km)")
        ax.set_ylabel("Elevation (m)")
        ax.grid(alpha=0.3)
        if len(pts) >= 2:
            d, z, _, _ = profile_along(self.da, pts, swath_halfwidth=self.swath_halfwidth)
            ax.plot(d / 1e3, z, color=self.color, lw=1.2)
            for i, (name, level) in enumerate(self.ref_levels.items()):
                ax.axhline(level, ls="--", lw=1, color=f"C{i}", label=f"{name} ({level:.0f} m)")
            if self.ref_levels:
                ax.legend(fontsize=8)
        elif is_interactive():
            ax.set_title("Click on the map to add points  (u = undo, c = clear)", fontsize=9)
        else:
            ax.set_title("⚠️ Interactive figures are OFF -- see Part 0", fontsize=9, color="crimson")
        self.fig.canvas.draw_idle()

    def get_profile(self):
        """(distance_m, elevation_m) along the line you drew."""
        if len(self.points) < 2:
            raise ValueError("Click at least two points on the map first.")
        d, z, _, _ = profile_along(self.da, self.points, swath_halfwidth=self.swath_halfwidth)
        return d, z


class PolygonEditor:
    """Interactive polygon tool (matplotlib PolygonSelector).

    * Click to add vertices; click on the FIRST vertex to close the polygon.
    * After closing: drag a vertex to move it, right-click a vertex to delete it,
      shift + drag to move the whole polygon, Esc to start again.
    * `.polygon` returns the polygon as a shapely Polygon.
    """

    def __init__(self, da, title="Draw a polygon", extent=None, step=4, color="cyan"):
        self.fig, self.ax = plt.subplots(figsize=(7, 6))
        plot_basemap(self.ax, da, step=step, extent=extent, colorbar=False)
        km_axes(self.ax)
        self.ax.set_title(title, fontsize=10)
        self.selector = PolygonSelector(
            self.ax, onselect=lambda verts: None,
            props=dict(color=color, lw=1.5),
            handle_props=dict(markersize=5, mec=color, mfc="none"))
        self.fig.tight_layout()

    def set_polygon(self, polygon):
        self.selector.verts = list(polygon.exterior.coords)[:-1]

    @property
    def polygon(self):
        verts = self.selector.verts
        if len(verts) < 3:
            raise ValueError("Draw a polygon on the map first (and close it by clicking its first vertex).")
        return Polygon(verts)