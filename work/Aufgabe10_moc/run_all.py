"""
Template for calling miniTopSim.

Feel free to copy, but do not modify the original!
"""

from mini_topsim.main import mini_topsim
from mini_topsim.plot import plot

mini_topsim('cosine_norm_noredep.cfg')
mini_topsim('cosine_moc_noredep.cfg')
mini_topsim('cosine_norm_redep.cfg')
mini_topsim('cosine_moc_redep.cfg')

mini_topsim('gauss_norm_noredep.cfg')
mini_topsim('gauss_moc_noredep.cfg')
mini_topsim('gauss_norm_redep.cfg')
mini_topsim('gauss_moc_redep.cfg')