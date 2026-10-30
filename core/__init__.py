"""Core simulation engines. No Streamlit imports in this package."""

from .registry import get_engine

__all__ = ["get_engine"]
