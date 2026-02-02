"""
ROYAL AVATAR SYSTEM
Player character with medical upgrade system

Integrates player avatar with progression mechanics and healing abilities
"""

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum
import random


class MedicalSpecialty(Enum):
    """Medical upgrade specializations"""
    BATTLEFIELD_MEDIC = "battlefield_medic"      # Quick healing
    ALCHEMIST = "alchemist"                      # Potion crafting
    CHIRURGEON = "chirurgeon"                    # Precise surgery
    HEALER_SAINT = "healer_saint"                # Holy restoration
    PLAGUE_DOCTOR = "plague_doctor"              # Disease cure
    PHYSICIAN = "physician"                      # Balanced medicine


class MedicalTier(Enum):
    """Medical upgrade progression tiers"""
    INITIATE = 1        # Basic healing
    APPRENTICE = 2      # Improved potions
    JOURNEYMAN = 3      # Specialty focus
    MASTER = 4          # Advanced techniques
    LEGENDARY = 5       # Mythic healing


@dataclass
class MedicalAbility:
    """Individual healing ability"""
    name: str
    specialty: MedicalSpecialty
    healing_power: int
    cooldown_turns: int
    mana_cost: int
    description: str
    tier_required: int


@dataclass
class RoyalAvatar:
    """Player character - Royal Healer Knight"""
    name: str
    level: int = 1
    max_health: int = 150
    current_health: int = 150
    mana: int = 100
    max_mana: int = 100
    
    # Medical system
    medical_specialty: MedicalSpecialty = MedicalSpecialty.BATTLEFIELD_MEDIC
    medical_tier: MedicalTier = MedicalTier.INITIATE
    medical_experience: int = 0
    medical_mastery: int = 0  # 0-100 per specialty
    
    # Combat stats
    attack: int = 12
    defense: int = 15
    magical_power: int = 18
    
    # Armor details
    armor_class: int = 18  # AC in D&D terms
    armor_material: str = "Enchanted Steel"
    armor_color: str = "Gold and Silver Filigree"
    
    # Healing inventory
    healing_potions: int = 5
    antidotes: int = 3
    restoration_scrolls: int = 2
    
    # Medical abilities unlocked
    abilities: List[MedicalAbility] = field(default_factory=list)
    active_specialty_abilities: Dict[str, MedicalAbility] = field(default_factory=dict)
    
    # Status tracking
    conditions: List[str] = field(default_factory=list)  # poisoned, bleeding, etc
    buffs: List[str] = field(default_factory=list)       # protected, strengthened, etc
    
    def __post_init__(self):
        """Initialize avatar with starter abilities"""
        self._initialize_starter_abilities()
    
    def _initialize_starter_abilities(self) -> None:
        """Create starter medical abilities"""
        self.abilities = [
            MedicalAbility(
                name="First Aid",
                specialty=MedicalSpecialty.BATTLEFIELD_MEDIC,
                healing_power=20,
                cooldown_turns=1,
                mana_cost=15,
                description="Quick battlefield healing for self or ally",
                tier_required=1
            ),
            MedicalAbility(
                name="Minor Restoration",
                specialty=MedicalSpecialty.PHYSICIAN,
                healing_power=15,
                cooldown_turns=2,
                mana_cost=10,
                description="Basic health restoration",
                tier_required=1
            ),
            MedicalAbility(
                name="Poison Purge",
                specialty=MedicalSpecialty.ALCHEMIST,
                healing_power=0,
                cooldown_turns=2,
                mana_cost=20,
                description="Remove poisoning and toxins",
                tier_required=1
            )
        ]
        
        # Set active abilities
        for ability in self.abilities:
            self.active_specialty_abilities[ability.name] = ability
    
    def take_damage(self, damage: int) -> None:
        """Reduce health by damage amount"""
        self.current_health = max(0, self.current_health - damage)
    
    def heal_self(self, amount: int) -> None:
        """Restore own health"""
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def use_mana(self, amount: int) -> bool:
        """Consume mana for ability"""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False
    
    def restore_mana(self, amount: int) -> None:
        """Restore mana after action"""
        self.mana = min(self.max_mana, self.mana + amount)
    
    def cast_healing_spell(self, ability_name: str) -> Dict:
        """
        Cast a healing ability
        Returns effect details
        """
        if ability_name not in self.active_specialty_abilities:
            return {
                'success': False,
                'message': f"Ability {ability_name} not available"
            }
        
        ability = self.active_specialty_abilities[ability_name]
        
        # Check mana
        if not self.use_mana(ability.mana_cost):
            return {
                'success': False,
                'message': f"Insufficient mana. Need {ability.mana_cost}, have {self.mana}"
            }
        
        # Apply healing
        healing_variance = random.randint(-5, 10)
        actual_healing = max(1, ability.healing_power + healing_variance)
        self.heal_self(actual_healing)
        
        return {
            'success': True,
            'ability': ability_name,
            'healing': actual_healing,
            'health_restored': self.current_health,
            'mana_spent': ability.mana_cost,
            'message': f"Cast {ability_name}! Healed {actual_healing} HP"
        }
    
    def use_healing_potion(self) -> Dict:
        """Use a potion from inventory"""
        if self.healing_potions <= 0:
            return {
                'success': False,
                'message': "No healing potions available"
            }
        
        healing_amount = random.randint(30, 50)
        self.heal_self(healing_amount)
        self.healing_potions -= 1
        
        return {
            'success': True,
            'healing': healing_amount,
            'health_restored': self.current_health,
            'potions_remaining': self.healing_potions,
            'message': f"Drank potion! Healed {healing_amount} HP ({self.healing_potions} potions left)"
        }
    
    def add_condition(self, condition: str) -> None:
        """Apply negative status condition"""
        if condition not in self.conditions:
            self.conditions.append(condition)
    
    def remove_condition(self, condition: str) -> None:
        """Remove status condition"""
        if condition in self.conditions:
            self.conditions.remove(condition)
    
    def add_buff(self, buff: str) -> None:
        """Apply positive buff"""
        if buff not in self.buffs:
            self.buffs.append(buff)
    
    def remove_buff(self, buff: str) -> None:
        """Remove buff"""
        if buff in self.buffs:
            self.buffs.remove(buff)
    
    def upgrade_medical_specialty(self) -> None:
        """Advance to next medical tier"""
        if self.medical_tier.value < 5:
            self.medical_tier = MedicalTier(self.medical_tier.value + 1)
            self._unlock_specialty_abilities()
    
    def _unlock_specialty_abilities(self) -> None:
        """Unlock new abilities at new tier"""
        tier_abilities = {
            MedicalTier.APPRENTICE: [
                MedicalAbility(
                    name="Improved Restoration",
                    specialty=MedicalSpecialty.PHYSICIAN,
                    healing_power=35,
                    cooldown_turns=2,
                    mana_cost=25,
                    description="Enhanced healing magic",
                    tier_required=2
                )
            ],
            MedicalTier.JOURNEYMAN: [
                MedicalAbility(
                    name="Specialty Mastery",
                    specialty=self.medical_specialty,
                    healing_power=50,
                    cooldown_turns=3,
                    mana_cost=35,
                    description=f"Master {self.medical_specialty.value} technique",
                    tier_required=3
                )
            ],
            MedicalTier.MASTER: [
                MedicalAbility(
                    name="Grand Healing",
                    specialty=MedicalSpecialty.HEALER_SAINT,
                    healing_power=75,
                    cooldown_turns=4,
                    mana_cost=50,
                    description="Powerful restoration magic",
                    tier_required=4
                )
            ],
            MedicalTier.LEGENDARY: [
                MedicalAbility(
                    name="Mythic Restoration",
                    specialty=MedicalSpecialty.HEALER_SAINT,
                    healing_power=100,
                    cooldown_turns=5,
                    mana_cost=75,
                    description="Legendary healing power",
                    tier_required=5
                )
            ]
        }
        
        new_abilities = tier_abilities.get(self.medical_tier, [])
        for ability in new_abilities:
            self.abilities.append(ability)
            self.active_specialty_abilities[ability.name] = ability
    
    def get_avatar_status(self) -> Dict:
        """Get complete avatar status"""
        return {
            'name': self.name,
            'level': self.level,
            'health': f"{self.current_health}/{self.max_health}",
            'mana': f"{self.mana}/{self.max_mana}",
            'armor': f"{self.armor_material} ({self.armor_color})",
            'armor_class': self.armor_class,
            'stats': {
                'attack': self.attack,
                'defense': self.defense,
                'magical_power': self.magical_power
            },
            'medical': {
                'specialty': self.medical_specialty.value,
                'tier': self.medical_tier.name,
                'mastery': self.medical_mastery
            },
            'abilities': list(self.active_specialty_abilities.keys()),
            'inventory': {
                'healing_potions': self.healing_potions,
                'antidotes': self.antidotes,
                'restoration_scrolls': self.restoration_scrolls
            },
            'conditions': self.conditions,
            'buffs': self.buffs
        }


class AvatarDisplay:
    """Display royal avatar with medical status"""
    
    def __init__(self, avatar: RoyalAvatar):
        self.avatar = avatar
    
    def render_avatar_portrait(self) -> str:
        """
        Render ASCII art representation of avatar
        Young girl in royal gold/silver armor with healer aesthetic
        """
        portrait = f"""
╔════════════════════════════════════════════════════════════════╗
║              ROYAL HEALER KNIGHT - {self.avatar.name.upper():^38} ║
║                                                                ║
║                    ⚔️ 👑 ✨                                     ║
║                                                                ║
║             🛡️  ARMORED HEALER  🛡️                           ║
║                                                                ║
║        Golden Filigree Steel Plate Armor                      ║
║        Young Royal Knight - Medical Master                    ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║ VITAL STATISTICS                                              ║
║ ─────────────────────────────────────────────────────────────  ║
║ Level: {self.avatar.level:<2d}  |  AC: {self.avatar.armor_class:<2d}  |  Medical Tier: {self.avatar.medical_tier.name:<12} ║
║ HP: {self.avatar.current_health:>3}/{self.avatar.max_health:<3}  |  MANA: {self.avatar.mana:>3}/{self.avatar.max_mana:<3}                       ║
║ ─────────────────────────────────────────────────────────────  ║
║ COMBAT STATS                                                  ║
║ ─────────────────────────────────────────────────────────────  ║
║ ATK: {self.avatar.attack:<2d}  |  DEF: {self.avatar.defense:<2d}  |  MAG: {self.avatar.magical_power:<2d}                       ║
║ ─────────────────────────────────────────────────────────────  ║
║ MEDICAL SPECIALTY: {self.avatar.medical_specialty.value:^36} ║
║ MASTERY LEVEL: {self.avatar.medical_mastery:<3}%                                     ║
║ ─────────────────────────────────────────────────────────────  ║
║ HEALING INVENTORY                                             ║
║ ─────────────────────────────────────────────────────────────  ║
║ Healing Potions: {self.avatar.healing_potions:<2d}  |  Antidotes: {self.avatar.antidotes:<2d}  |  Scrolls: {self.avatar.restoration_scrolls:<2d}     ║
║ ─────────────────────────────────────────────────────────────  ║
║ AVAILABLE ABILITIES ({len(self.avatar.active_specialty_abilities)})                                     ║
"""
        
        for i, ability_name in enumerate(self.avatar.active_specialty_abilities.keys(), 1):
            ability = self.avatar.active_specialty_abilities[ability_name]
            portrait += f"║ {i}. {ability_name:<50} [Mana: {ability.mana_cost:<2}] ║\n"
        
        portrait += """║ ─────────────────────────────────────────────────────────────  ║"""
        
        if self.avatar.conditions:
            portrait += f"\n║ CONDITIONS: {', '.join(self.avatar.conditions):<43} ║"
        
        if self.avatar.buffs:
            portrait += f"\n║ BUFFS: {', '.join(self.avatar.buffs):<50} ║"
        
        portrait += "\n╚════════════════════════════════════════════════════════════════╝"
        
        return portrait
    
    def render_health_bar(self) -> str:
        """Render health bar visualization"""
        bar_length = 30
        filled = int((self.avatar.current_health / self.avatar.max_health) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        return f"HP: [{bar}] {self.avatar.current_health}/{self.avatar.max_health}"
    
    def render_mana_bar(self) -> str:
        """Render mana bar visualization"""
        bar_length = 30
        filled = int((self.avatar.mana / self.avatar.max_mana) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        return f"MANA: [{bar}] {self.avatar.mana}/{self.avatar.max_mana}"


def create_player_avatar(name: str = "Royal Healer") -> RoyalAvatar:
    """Factory function to create new avatar"""
    avatar = RoyalAvatar(
        name=name,
        level=1,
        max_health=150,
        current_health=150,
        mana=100,
        max_mana=100,
        medical_specialty=MedicalSpecialty.BATTLEFIELD_MEDIC,
        medical_tier=MedicalTier.INITIATE
    )
    return avatar
