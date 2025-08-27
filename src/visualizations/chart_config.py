import matplotlib.pyplot as plt
import seaborn as sns

# Standardized chart style
sns.set_theme(style="whitegrid")

CHART_SIZE = (10, 6)
CHART_DPI = 120
CHART_COLORS = sns.color_palette("Set2")

# Apply global matplotlib settings
def apply_chart_style():
    plt.rcParams["figure.figsize"] = CHART_SIZE
    plt.rcParams["figure.dpi"] = CHART_DPI
    plt.rcParams["axes.prop_cycle"] = plt.cycler(color=CHART_COLORS)
    plt.rcParams["axes.titlesize"] = 16
    plt.rcParams["axes.labelsize"] = 14
    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12
    plt.rcParams["legend.fontsize"] = 12
    plt.rcParams["legend.frameon"] = True
    plt.rcParams["axes.grid"] = True 