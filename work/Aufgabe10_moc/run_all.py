"""
Script to run all necessary simulations consecutively
"""

from mini_topsim.main import mini_topsim

mini_topsim('cosine_norm_noredep.cfg')
mini_topsim('cosine_moc_noredep.cfg')
mini_topsim('cosine_norm_redep.cfg')
mini_topsim('cosine_moc_redep.cfg')

mini_topsim('gauss_norm_noredep.cfg')
mini_topsim('gauss_moc_noredep.cfg')
mini_topsim('gauss_norm_redep.cfg')
mini_topsim('gauss_moc_redep.cfg')