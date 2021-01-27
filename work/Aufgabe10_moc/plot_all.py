"""
Script to plot all necessary simulations
"""

from mini_topsim.plot import plot

plot('cosine_norm_noredep.srf', 'cosine_moc_noredep.srf')
plot('cosine_norm_redep.srf', 'cosine_moc_redep.srf')

plot('gauss_norm_noredep.srf', 'gauss_moc_noredep.srf')
plot('gauss_norm_redep.srf', 'gauss_moc_redep.srf')
