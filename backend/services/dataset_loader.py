
# This keeps startup fast and only uses memory if/when the dataset is needed. 
# If you later want background startup loading, add a FastAPI startup event to pre-load it.

"""Helper for loading the veterinary dataset with a lazy (cached) loader.

Usage:
    from backend.services.dataset_loader import get_vet_dataset
    ds = get_vet_dataset()

This module loads the dataset on first use and caches it in memory. Loading can
be slow and memory-heavy, so lazy loading avoids startup delays unless the
dataset is actually needed.
"""
import logging
from datasets import load_dataset

# Module-level cache for the loaded dataset. Starts as None and is populated
# on the first successful call to `get_vet_dataset()`.
_VET_DATASET = None


def load_vet_dataset():
    """Perform the actual dataset download/load and return the dataset object.

    This function may raise exceptions from the `datasets` library (network
    errors, missing dataset, etc.). Callers that want resilience should use
    `get_vet_dataset()` which catches errors and returns None on failure.
    """
    # Delegates to the `datasets` library to obtain the named dataset split.
    return load_dataset("viggovet/Veterinary-Med", split="train")


def get_vet_dataset():
    """Return the cached dataset, loading it on first call.

    Behavior:
    - If the dataset is already loaded, return it immediately (fast).
    - On first call, attempt to load via `load_vet_dataset()` and cache result.
    - If loading fails, log the exception and return None (caller should
      handle a None result).

    This pattern keeps application startup fast and only uses memory when the
    dataset is actually required.
    """
    global _VET_DATASET
    if _VET_DATASET is None:
        try:
            # Load and cache the dataset (may block while downloading/initializing).
            _VET_DATASET = load_vet_dataset()
        except Exception as exc:
            # Record the exception for debugging; keep running but return None.
            logging.getLogger(__name__).exception("Failed to load vet dataset: %s", exc)
            _VET_DATASET = None
    return _VET_DATASET