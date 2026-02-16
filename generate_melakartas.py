"""
Generate all 72 Melakarta Ragas programmatically

Melakarta system:
- 6 chakras (groups) × 6 ragas each = 36 ragas (Suddha Madhyama)
- 6 chakras (groups) × 6 ragas each = 36 ragas (Prati Madhyama)
Total = 72 ragas

Swara structure:
- R: R1 (1), R2 (2), R3 (3)
- G: G1 (3), G2 (4), G3 (4) 
- M: M1 (5), M2 (6)
- D: D1 (8), D2 (9), D3 (10)
- N: N1 (10), N2 (11), N3 (11)

Rules:
- If R1 → G can be G1, G2, or G3
- If R2 → G can be G2 or G3  
- If R3 → G must be G3
- Same logic for D and N
"""

# All 72 Melakarta raga names in order
MELAKARTA_NAMES = [
    # Chakra 1 (Indu) - R1 combinations
    "Kanakangi", "Ratnangi", "Ganamurti", "Vanaspati", "Manavati", "Tanarupi",
    
    # Chakra 2 (Netra) - R2/G2 combinations  
    "Senavati", "Hanumattodi", "Dhenuka", "Natakapriya", "Kokilapriya", "Rupavati",
    
    # Chakra 3 (Agni) - R2/G3 combinations
    "Gayakapriya", "Vakulabharanam", "Mayamalavagowla", "Chakravakam", "Suryakantam", "Hatakambari",
    
    # Chakra 4 (Veda) - R3/G3 combinations
    "Jhankaradhwani", "Natabhairavi", "Kiravani", "Kharaharapriya", "Gourimanohari", "Varunapriya",
    
    # Chakra 5 (Bana) - R3/G3 combinations
    "Mararanjani", "Charukesi", "Sarasangi", "Harikambhoji", "Dheerasankarabharanam", "Naganandini",
    
    # Chakra 6 (Rutu) - R3/G3 combinations  
    "Yagapriya", "Ragavardhani", "Gangeyabhushani", "Vagadheeswari", "Shulini", "Chalanata",
    
    # Chakra 7 (Rishi) - Prati Madhyama - R1 combinations
    "Salagam", "Jalarnavam", "Jhalavarali", "Navaneetam", "Pavani", "Raghupriya",
    
    # Chakra 8 (Vasu) - Prati Madhyama - R2/G2 combinations
    "Gavambodhi", "Bhavapriya", "Shubhapantuvarali", "Shadvidamargini", "Suvarnangi", "Divyamani",
    
    # Chakra 9 (Brahma) - Prati Madhyama - R2/G3 combinations  
    "Dhavalambari", "Namanarayani", "Kamavardhani", "Ramapriya", "Gamanashrama", "Viswambari",
    
    # Chakra 10 (Disi) - Prati Madhyama - R3/G3 combinations
    "Shyamalangi", "Shanmukhapriya", "Simhendramadhyamam", "Hemavati", "Dharmavati", "Neetimati",
    
    # Chakra 11 (Rudra) - Prati Madhyama - R3/G3 combinations
    "Kantamani", "Rishabhapriya", "Latangi", "Vachaspati", "Mechakalyani", "Chitrambari",
    
    # Chakra 12 (Aditya) - Prati Madhyama - R3/G3 combinations
    "Sucharitra", "Jyotiswarupini", "Dhatuvardhani", "Nasikabhushani", "Kosalam", "Rasikapriya"
]


def get_melakarta_structure(raga_number):
    """
    Returns the swara structure for a given Melakarta number (1-72).
    
    Returns:
        swaras: List of swara names
        intervals: List of semitone intervals from Sa
    """
    # Determine if Suddha Madhyama (1-36) or Prati Madhyama (37-72)
    if raga_number <= 36:
        M = 'M1'
        M_int = 5
        adjusted_num = raga_number
    else:
        M = 'M2'
        M_int = 6
        adjusted_num = raga_number - 36
    
    # Determine Chakra (1-6) and position within chakra (1-6)
    chakra = (adjusted_num - 1) // 6 + 1
    position = (adjusted_num - 1) % 6 + 1
    
    # Determine R and G based on chakra
    if chakra == 1:
        R, G = 'R1', ['G1', 'G2', 'G3'][position - 1] if position <= 3 else ['G1', 'G2', 'G3'][(position - 4)]
        R_int = 1
        G_int = [3, 4, 4][min(position - 1, 2)]
    elif chakra == 2:
        R, G = 'R1', ['G1', 'G2', 'G3'][position - 1] if position <= 3 else ['G1', 'G2', 'G3'][(position - 4)]
        R_int = 1
        G_int = [3, 4, 4][min(position - 1, 2)]
    elif chakra == 3:
        R = 'R2'
        R_int = 2
        G = 'G2' if position <= 3 else 'G3'
        G_int = 4 if position <= 3 else 4
    elif chakra == 4:
        R = 'R2'
        R_int = 2
        G = 'G3'
        G_int = 4
    elif chakra == 5:
        R = 'R3'
        R_int = 3
        G = 'G3'
        G_int = 4
    else:  # chakra == 6
        R = 'R3'
        R_int = 3
        G = 'G3'
        G_int = 4
    
    # Determine D and N based on position within chakra (same logic as R-G)
    if position == 1:
        D, N = 'D1', 'N1'
        D_int, N_int = 8, 10
    elif position == 2:
        D, N = 'D1', 'N2'
        D_int, N_int = 8, 11
    elif position == 3:
        D, N = 'D1', 'N3'
        D_int, N_int = 8, 11
    elif position == 4:
        D, N = 'D2', 'N2'
        D_int, N_int = 9, 11
    elif position == 5:
        D, N = 'D2', 'N3'
        D_int, N_int = 9, 11
    else:  # position == 6
        D, N = 'D3', 'N3'
        D_int, N_int = 10, 11
    
    swaras = ['S', R, G, M, 'P', D, N]
    intervals = [0, R_int, G_int, M_int, 7, D_int, N_int]
    
    return swaras, intervals


def generate_all_melakartas():
    """Generate dictionary of all 72 Melakarta ragas."""
    melakartas = {}
    
    for i in range(1, 73):
        name = MELAKARTA_NAMES[i - 1]
        swaras, intervals = get_melakarta_structure(i)
        
        melakartas[name] = {
            'swaras': swaras,
            'key_intervals': intervals,
            'description': f'{i}th Melakarta raga'
        }
    
    return melakartas


def generate_python_code():
    """Generate Python code to paste into raga_detector.py"""
    melakartas = generate_all_melakartas()
    
    print("# Copy this and replace the RAGA_PATTERNS dictionary in raga_detector.py\n")
    print("RAGA_PATTERNS = {")
    
    for name, info in melakartas.items():
        print(f"    '{name}': {{")
        print(f"        'swaras': {info['swaras']},")
        print(f"        'key_intervals': {info['key_intervals']},")
        print(f"        'description': '{info['description']}'")
        print("    },")
    
    print("}")


def test_known_ragas():
    """Test some well-known Melakartas to verify correctness."""
    print("\n" + "="*70)
    print("TESTING WELL-KNOWN MELAKARTAS")
    print("="*70 + "\n")
    
    test_cases = {
        15: ("Mayamalavagowla", ['S', 'R1', 'G3', 'M1', 'P', 'D1', 'N3'], [0, 1, 4, 5, 7, 8, 11]),
        28: ("Harikambhoji", ['S', 'R2', 'G3', 'M1', 'P', 'D2', 'N2'], [0, 2, 4, 5, 7, 9, 10]),
        29: ("Dheerasankarabharanam", ['S', 'R2', 'G3', 'M1', 'P', 'D2', 'N3'], [0, 2, 4, 5, 7, 9, 11]),
        65: ("Mechakalyani", ['S', 'R2', 'G3', 'M2', 'P', 'D2', 'N3'], [0, 2, 4, 6, 7, 9, 11]),
        20: ("Natabhairavi", ['S', 'R2', 'G2', 'M1', 'P', 'D2', 'N2'], [0, 2, 3, 5, 7, 9, 10]),
    }
    
    for num, (expected_name, expected_swaras, expected_intervals) in test_cases.items():
        swaras, intervals = get_melakarta_structure(num)
        actual_name = MELAKARTA_NAMES[num - 1]
        
        name_match = "✓" if actual_name == expected_name else "✗"
        swara_match = "✓" if swaras == expected_swaras else "✗"
        interval_match = "✓" if intervals == expected_intervals else "✗"
        
        print(f"Melakarta #{num}: {actual_name}")
        print(f"  Name:      {name_match} Expected: {expected_name}")
        print(f"  Swaras:    {swara_match} {swaras}")
        print(f"  Intervals: {interval_match} {intervals}")
        print()


if __name__ == "__main__":
    # Run tests first
    test_known_ragas()
    
    # Generate the code
    print("\n" + "="*70)
    print("GENERATING CODE FOR RAGA_DETECTOR.PY")
    print("="*70 + "\n")
    
    generate_python_code()
    
    print("\n" + "="*70)
    print(f"✓ Successfully generated all {len(MELAKARTA_NAMES)} Melakarta ragas!")
    print("="*70)
