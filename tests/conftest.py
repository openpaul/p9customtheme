import tempfile
from pathlib import Path

from matplotlib.testing.compare import compare_images
from plotnine import ggplot

LOCAL_FOLDER = Path(__file__).parent
BASELINE_IMAGES = LOCAL_FOLDER / "baseline"


# Simplified and not as robust plotnine comparison
# Should be enough for this theme for now
def ggplot_equals(plot: ggplot, name: str) -> bool:
    reference = BASELINE_IMAGES / f"{name}.png"
    if not reference.exists():
        plot.save(reference, verbose=False)
        raise FileNotFoundError(
            f"Reference image {reference} does not exist, this is now the new reference! Check it and rerun"
        )
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfile = Path(tmpdirname) / "test.png"
        plot.save(tmpfile, verbose=False)
        return compare_images(str(reference), str(tmpfile), tol=1e-3) is None


ggplot.__eq__ = ggplot_equals  # type: ignore # to make the monkey patching work
