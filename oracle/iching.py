import secrets

# Hexagram data: number, name, meaning
HEXAGRAMS = {
    1: ("The Creative", "Pure creative force, strength, leadership, dynamic power."),
    2: ("The Receptive", "Receptive energy, support, nurturing, adaptability."),
    3: ("Difficulty at the Beginning", "Initial hardship, growing pains, perseverance."),
    4: ("Youthful Folly", "Inexperience, need for guidance, openness to learning."),
    5: ("Waiting (Nourishment)", "Patience, preparation, trust in timing."),
    6: ("Conflict", "Confrontation, differences of opinion, resolution."),
    7: ("The Army", "Discipline, collective effort, leadership, strategy."),
    8: ("Holding Together (Union)", "Unity, belonging, shared purpose."),
    9: ("Small Taming Power", "Gentle influence, small gains, cautious progress."),
    10: ("Treading (Conduct)", "Careful action, respect, appropriate behavior."),
    11: ("Peace", "Harmony, balance, prosperity, natural flow."),
    12: ("Standstill (Stagnation)", "Obstacle, pause, potential for renewal."),
    13: ("Fellowship", "Community, shared goals, collaboration."),
    14: ("Possession in Great Measure", "Abundance, success, wise management."),
    15: ("Modesty", "Humility, balance, restraint, quiet strength."),
    16: ("Enthusiasm", "Energy, inspiration, forward momentum."),
    17: ("Following", "Adaptability, alignment with circumstances."),
    18: ("Work on What Has Been Spoiled", "Restoration, correction, repair."),
    19: ("Approach", "Progress, opportunity, positive growth."),
    20: ("Contemplation (View)", "Reflection, awareness, broadened perspective."),
    21: ("Biting Through", "Resolving obstacles, decisive action."),
    22: ("Grace", "Elegance, beauty, harmonious presentation."),
    23: ("Splitting Apart", "Decline, disintegration, facing endings."),
    24: ("Return (The Turning Point)", "Renewal, new beginnings, return to the source."),
    25: ("Innocence (The Unexpected)", "Spontaneity, simplicity, openness."),
    26: ("Taming the Power of the Great", "Harnessing great energy, careful restraint."),
    27: ("Nourishment", "Care, sustenance, mindful consumption."),
    28: ("Preponderance of the Great", "Critical mass, pivotal moment, burden."),
    29: ("The Abysmal (Water)", "Danger, perseverance through hardship."),
    30: ("The Clinging (Fire)", "Illumination, clarity, dependent energy."),
    31: ("Influence (Wooing)", "Attraction, influence, subtle persuasion."),
    32: ("Duration", "Consistency, endurance, ongoing effort."),
    33: ("Retreat", "Strategic withdrawal, regrouping."),
    34: ("The Power of the Great", "Great strength, leadership, exertion."),
    35: ("Progress", "Advancement, growth, development."),
    36: ("Darkening of the Light", "Caution, perseverance under adversity."),
    37: ("The Family", "Social roles, community, relationships."),
    38: ("Opposition", "Contradictions, finding harmony in difference."),
    39: ("Obstruction", "Challenges, detours, persistence."),
    40: ("Deliverance", "Relief, release from tension, solution."),
    41: ("Decrease", "Simplicity, focus, conservation."),
    42: ("Increase", "Growth, abundance, opportunity."),
    43: ("Breakthrough", "Decisive advance, resolution."),
    44: ("Coming to Meet", "Encountering opportunity or challenge."),
    45: ("Gathering Together (Massing)", "Congregation, collective strength."),
    46: ("Pushing Upward", "Ambition, determined effort."),
    47: ("Oppression (Exhaustion)", "Fatigue, hardship, inner strength."),
    48: ("The Well", "Source of nourishment, shared resources."),
    49: ("Revolution (Molting)", "Transformation, renewal."),
    50: ("The Cauldron", "Transformation, nurturing of excellence."),
    51: ("The Arousing (Shock)", "Sudden shock, awakening."),
    52: ("Keeping Still (Mountain)", "Stillness, meditation, inner peace."),
    53: ("Development (Gradual Progress)", "Steady progress, natural evolution."),
    54: ("The Marrying Maiden", "Adaptation, secondary roles, caution."),
    55: ("Abundance", "Prosperity, fullness, radiance."),
    56: ("The Wanderer", "Travel, transition, adaptability."),
    57: ("The Gentle (Wind)", "Penetrating influence, subtle progress."),
    58: ("The Joyous (Lake)", "Joy, open communication, positive energy."),
    59: ("Dispersion (Dissolution)", "Dispersal of obstacles, liberation."),
    60: ("Limitation", "Boundaries, discipline, regulation."),
    61: ("Inner Truth", "Sincerity, authenticity, integrity."),
    62: ("Preponderance of the Small", "Attention to detail, cautious progress."),
    63: ("After Completion", "Success followed by vigilance."),
    64: ("Before Completion", "Approaching success, remaining alert."),
}

def throw_coins():
    return [secrets.choice([2, 3]) for _ in range(6)]  # bottom to top

def render_hexagram(lines):
    return "\n".join(["⚋⚋" if l == 2 else "⚊⚊" for l in reversed(lines)])  # top to bottom

def hexagram_number(lines):
    # Convert lines (2 or 3) to binary: 2 -> 0, 3 -> 1
    binary = ''.join(['0' if l == 2 else '1' for l in reversed(lines)])  # top to bottom
    return int(binary, 2) + 1  # Hexagrams are numbered 1–64

def get_hexagram_info(number):
    return HEXAGRAMS.get(number, ("Unknown Hexagram", "No interpretation available."))

if __name__ == "__main__":
    lines = throw_coins()
    hexagram = render_hexagram(lines)
    number = hexagram_number(lines)
    name, meaning = get_hexagram_info(number)

    print(f"Today's Hexagram: #{number} - {name}")
    print(hexagram)
    print(f"Meaning: {meaning}")

