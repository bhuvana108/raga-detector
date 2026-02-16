"""
Simple Carnatic Raga Detection System

This system extracts pitch features from audio and uses basic pattern matching
to identify common Carnatic ragas.
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mode
from pathlib import Path

'''
'''
# Define raga characteristics (simplified - based on dominant swaras)
RAGA_PATTERNS = {
    'Mohanam': {
        'swaras': ['S', 'R2', 'G3', 'P', 'D2'],  # Pentatonic
        'key_intervals': [0, 2, 4, 7, 9],  # In semitones from Sa
        'description': 'Janya of Harikambhoji, all shuddha swaras'
    },
    'Mayamalavagowla': {
        'swaras': ['S', 'R1', 'G3', 'M1', 'P', 'D1', 'N3'],
        'key_intervals': [0, 1, 4, 5, 7, 8, 11],
        'description': '15th Melakarta, morning raga'
    },
    'Shankarabharanam': {
        'swaras': ['S', 'R2', 'G3', 'M1', 'P', 'D2', 'N3'],
        'key_intervals': [0, 2, 4, 5, 7, 9, 11],  # Major scale
        'description': '29th Melakarta, very common'
    },
    'Kalyani': {
        'swaras': ['S', 'R2', 'G3', 'M2', 'P', 'D2', 'N3'],
        'key_intervals': [0, 2, 4, 6, 7, 9, 11],  # Lydian mode
        'description': '65th Melakarta, auspicious raga'
    },
    'Bhairavi': {
        'swaras': ['S', 'R1', 'G2', 'M1', 'P', 'D1', 'N2'],
        'key_intervals': [0, 1, 3, 5, 7, 8, 10],
        'description': '20th Melakarta, evening raga'
    }
}



class RagaDetector:
    def __init__(self, audio_path):
        """Initialize the raga detector with an audio file."""
        self.audio_path = audio_path
        self.y, self.sr = librosa.load(audio_path, sr=22050)
        self.duration = librosa.get_duration(y=self.y, sr=self.sr)
        
    def extract_pitch(self):
        """Extract pitch using pYIN algorithm."""
        print("Extracting pitch contour...")
        
        # pYIN is better for vocal/monophonic pitch detection
        f0, voiced_flag, voiced_probs = librosa.pyin(
            self.y,
            fmin=librosa.note_to_hz('C2'),  # ~65 Hz
            fmax=librosa.note_to_hz('C7'),  # ~2093 Hz
            sr=self.sr
        )
        
        # Remove unvoiced segments
        f0_clean = f0[voiced_flag]
        
        return f0, f0_clean
    
    def find_tonic(self, f0_clean):
        """Estimate the tonic (Sa) frequency."""
        print("Finding tonic (Sa)...")
        
        # Use histogram method to find most common pitch
        hist, bins = np.histogram(f0_clean, bins=100)
        tonic_hz = bins[np.argmax(hist)]
        
        print(f"Estimated tonic: {tonic_hz:.2f} Hz ({librosa.hz_to_note(tonic_hz)})")
        return tonic_hz
    
    def extract_swara_distribution(self, f0_clean, tonic_hz):
        """Convert pitches to chromatic scale relative to tonic."""
        # Convert Hz to cents relative to tonic
        cents = 1200 * np.log2(f0_clean / tonic_hz)
        
        # Wrap to single octave (0-1200 cents)
        cents_wrapped = cents % 1200
        
        # Quantize to 12-tone chromatic scale
        semitones = np.round(cents_wrapped / 100).astype(int) % 12
        
        # Create histogram of semitone usage
        swara_dist = np.bincount(semitones, minlength=12)
        swara_dist = swara_dist / swara_dist.sum()  # Normalize
        
        return swara_dist
    
    def match_raga(self, swara_dist):
        """Match the swara distribution to known ragas."""
        print("\nMatching to known ragas...")
        
        scores = {}
        for raga_name, raga_info in RAGA_PATTERNS.items():
            # Create ideal distribution for this raga
            raga_profile = np.zeros(12)
            for interval in raga_info['key_intervals']:
                raga_profile[interval] = 1.0
            raga_profile = raga_profile / raga_profile.sum()
            
            # Calculate similarity (correlation coefficient)
            score = np.corrcoef(swara_dist, raga_profile)[0, 1]
            scores[raga_name] = score
        
        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked
    
    def visualize(self, f0, swara_dist):
        """Create visualizations of the analysis."""
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot 1: Pitch contour
        times = librosa.times_like(f0, sr=self.sr)
        axes[0].plot(times, f0, linewidth=0.5)
        axes[0].set_xlabel('Time (s)')
        axes[0].set_ylabel('Frequency (Hz)')
        axes[0].set_title('Pitch Contour')
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Swara distribution
        swara_names = ['S', 'R1/r', 'R2/g', 'G2', 'G3/m', 'M1', 
                       'M2/p', 'P', 'D1/d', 'D2/n', 'N2', 'N3']
        axes[1].bar(range(12), swara_dist)
        axes[1].set_xlabel('Swara (relative to tonic)')
        axes[1].set_ylabel('Normalized Frequency')
        axes[1].set_title('Swara Distribution')
        axes[1].set_xticks(range(12))
        axes[1].set_xticklabels(swara_names, rotation=45)
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('raga_analysis.png', dpi=150, bbox_inches='tight')
        print("\nVisualization saved as 'raga_analysis.png'")
        plt.close()
    
    def analyze(self):
        """Run complete raga detection analysis."""
        print(f"\n{'='*60}")
        print(f"Analyzing: {Path(self.audio_path).name}")
        print(f"Duration: {self.duration:.2f} seconds")
        print(f"{'='*60}\n")
        
        # Extract pitch
        f0, f0_clean = self.extract_pitch()
        
        if len(f0_clean) == 0:
            print("ERROR: No pitch detected! Make sure the audio has clear melodic content.")
            return
        
        # Find tonic
        tonic_hz = self.find_tonic(f0_clean)
        
        # Extract swara distribution
        swara_dist = self.extract_swara_distribution(f0_clean, tonic_hz)
        
        # Match to ragas
        matches = self.match_raga(swara_dist)
        
        # Display results
        print(f"\n{'='*60}")
        print("RAGA DETECTION RESULTS")
        print(f"{'='*60}")
        
        for i, (raga, score) in enumerate(matches, 1):
            percentage = score * 100
            bar = '█' * int(percentage / 5) + '░' * (20 - int(percentage / 5))
            print(f"\n{i}. {raga:20} {bar} {percentage:5.1f}%")
            print(f"   {RAGA_PATTERNS[raga]['description']}")
            print(f"   Swaras: {', '.join(RAGA_PATTERNS[raga]['swaras'])}")
        
        print(f"\n{'='*60}\n")
        
        # Create visualization
        self.visualize(f0, swara_dist)
        
        return matches[0][0]  # Return top match


def main():
    """Example usage."""
    print("\n" + "="*60)
    print("CARNATIC RAGA DETECTOR")
    print("="*60)
    
    # Get audio file path from user
    audio_path = input("\nEnter path to audio file (or 'demo' for test): ").strip()
    
    if audio_path.lower() == 'demo':
        print("\nTo use this detector:")
        print("1. Record or find a Carnatic music clip (vocal or instrumental)")
        print("2. Save it as WAV or MP3")
        print("3. Run this script again with the file path")
        return
    
    # Check if file exists
    if not Path(audio_path).exists():
        print(f"\nERROR: File not found: {audio_path}")
        return
    
    # Run detection
    detector = RagaDetector(audio_path)
    top_raga = detector.analyze()
    
    print(f"✓ Most likely raga: {top_raga}")


if __name__ == "__main__":
    main()