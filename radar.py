import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` Axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding Axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


# Corrected data structure
data = [
    ['Avg cost sat', 'Gini', 'CC score', 'FS ratio', 'FS dist'],
    ('Average ', [
        [252956, 1/0.431, 0.804, 0.368, 1/991],
        [346844, 1/0.409, 0.874, 0.513, 1/941],
        [215751, 1/0.441, 0.799, 0.371, 1/978],
    ]),
    ('Median ', [
        [84402.87840540273, 1/0.2749635696596563, 0.9731826735989282, 0.8359275263185326, 1/161.63234298262336],
        [83014.35080210872, 1/0.2918093085328118, 0.9609993130994479, 0.7712006061223895, 1/161.63234298262336],
        [84402.87840540273, 1/0.2749635696596563, 0.9731826735989282, 0.8357111323440538, 1/161.35144410621888],
    ])
]


# Function to normalize data separately for each radar plot
def normalize_data_separately(data_list):
    normalized_data = []
    normalized_data.append(data_list[0])  # Add categories
    
    # Normalize each case separately
    for title, case_data in data_list[1:]:
        # Convert to numpy array for easier operations
        case_array = np.array(case_data)
        
        # Find min and max for each category within this case
        min_vals = np.min(case_array, axis=0)
        max_vals = np.max(case_array, axis=0)
        
        # Avoid division by zero
        range_vals = max_vals - min_vals
        range_vals[range_vals == 0] = 1
        
        # Normalize this case's data
        normalized_case = []
        for d in case_data:
            normalized_d = (np.array(d)) / max_vals
            normalized_case.append(normalized_d.tolist())
        
        normalized_data.append((title, normalized_case))
    
    return normalized_data

# Use the new normalization function
normalized_data = normalize_data_separately(data)

N = 5
theta = radar_factory(N, frame='polygon')
spoke_labels = normalized_data.pop(0)

fig, axs = plt.subplots(figsize=(12, 6), nrows=1, ncols=2,
                        subplot_kw=dict(projection='radar'))
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

colors = ['b', 'r', 'g','y']
# Plot the two cases from the data on separate Axes
for ax, (title, case_data) in zip(axs.flat, normalized_data):
    ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d, color in zip(case_data, colors):
        ax.plot(theta, d, color=color)
        #ax.fill(theta, d, facecolor=color, alpha=0.25)
    ax.set_varlabels(spoke_labels)

# Add legend
labels = ('MES', 'MES comp', 'GB')
legend = axs[0].legend(labels, loc=(0.9, .95),
                      labelspacing=0.1, fontsize='small')

fig.text(0.5, 0.965, 'Rules comparison with normalized data (Gini and FS dist are inverted)',
         horizontalalignment='center', color='black', weight='bold',
         size='large')

plt.show()