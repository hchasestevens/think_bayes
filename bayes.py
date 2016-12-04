"""Wrappers around thinkbayes.py"""

from contextlib import contextmanager

from thinkbayes import *


@contextmanager
def normalized(p=None):
    """
    Normalize PMF after operations. 
    New PMF will be instantiated if not provided.
    """
    p_ = Pmf() if p is None else p
    yield p_
    p_.Normalize()


def pmf_counter(seq):
    """Return normalized distribution over item counts."""
    with normalized() as p:
        incr = p.Incr
        for item in seq:
            incr(item, 1)
        return p


def pmf(*args, **kwargs):
    """
    Convenience factory function for Pmfs.
    
    If args provided: even distribution over items.
    If kwargs used: distribution as specified.
    """
    assert not (args and kwargs), "Please supply only args or kwargs."
    
    if args:
        prob = 1 / float(len(args))
        kwargs = {item: prob for item in args}
        
    with normalized() as p:
        set_ = p.Set
        for item, prob in kwargs.items():
            set_(item, float(prob))
        return p
    