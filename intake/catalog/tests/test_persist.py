import os
import posixpath
import pytest

import intake


path = posixpath.dirname(__file__)


def test_idempotent(temp_cache):
    cat = intake.open_catalog(posixpath.abspath(
        posixpath.join(path, '..', '..', 'source', 'tests', 'sources.yaml')))
    s = cat.zarr1()
    assert not s.has_been_persisted
    s2 = s.persist()
    assert s.has_been_persisted
    assert not s.is_persisted
    assert not s2.has_been_persisted
    assert s2.is_persisted
    s3 = s.persist()
    assert s3 == s2


def test_parquet(temp_cache):
    inp = pytest.importorskip('intake_parquet')
    cat = intake.open_catalog(posixpath.abspath(
        posixpath.join(path, 'catalog1.yml')))
    s = cat.entry1()
    s2 = s.persist()
    assert isinstance(s2, inp.ParquetSource)