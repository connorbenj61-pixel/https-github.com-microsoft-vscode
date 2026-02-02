"""
Opponents package - AI adversaries for Amalgamation Game
"""

from .necromancer_opponent import NecromancerOpponent
from .guardian_opponent import RoyalGuardianOpponent
from .chess_3d_opponent import Chess3DOpponent

__all__ = [
    'NecromancerOpponent',
    'RoyalGuardianOpponent',
    'Chess3DOpponent'
]
