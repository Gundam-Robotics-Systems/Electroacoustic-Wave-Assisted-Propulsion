#!/usr/bin/env python3
import os
from solid import scad_render, cylinder, cube, union, difference, translate, rotate

class LockheedArmoredShieldGenerator:
    """
    Procedurally compiles a hollow armored containment shield whose longitudinal length
    is resonance-matched to acoustic wavelengths, featuring Lockheed style structural mounts.
    """
    def __init__(self, fundamental_frequency_hz: float = 13.72):
        self.speed_of_sound_m_s = 343.0
        self.frequency = fundamental_frequency_hz
        
        # Calculate precise half-wavelength multiple for structural shield length (in mm)
        self.wavelength_mm = (self.speed_of_sound_m_s / self.frequency) * 1000.0
        self.shield_length_mm = self.wavelength_mm * 1.0  # Full wavelength matching node (n=2 node profile)
        
        self.inner_core_diameter_mm = 12500.0  # Mates with the 12.5m open design core
        self.shield_thickness_mm = 400.0       # Hollow armor layer thickness profile
        self.output_dir = "gantry_templates"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def compile_shield_mesh(self) -> str:
        """Assembles the open-ended hollow armor jacket with Lockheed structural mounting brackets."""
        inner_r = self.inner_core_diameter_mm / 2.0
        outer_r = inner_r + self.shield_thickness_mm
        
        # 1. Hollow Armored Outer Shield (Open at intake and exit ends)
        outer_casing = cylinder(r=outer_r, h=self.shield_length_mm, center=True, segments=120)
        inner_clearance_bore = cylinder(r=inner_r, h=self.shield_length_mm + 10, center=True, segments=120)
        
        hollow_shield_jacket = difference()(outer_casing, inner_clearance_bore)
        
        # 2. Lockheed-Style Heavy Mounting Kits (Flush-mating base plates with anchor bolt holes)
        mounting_bracket_left = translate([-(outer_r + 300), 0, 0])(
            cube([600, 1200, self.shield_length_mm * 0.4], center=True)
        )
        mounting_bracket_right = translate([(outer_r + 300), 0, 0])(
            cube([600, 1200, self.shield_length_mm * 0.4], center=True)
        )
        
        # Drill anchor pattern through the mounting kits to match Lockheed frame rail indexing
        bolt_hole_left = translate([-(outer_r + 300), 0, 0])(
            cylinder(r=100, h=self.shield_length_mm, center=True, segments=30)
        )
        bolt_hole_right = translate([(outer_r + 300), 0, 0])(
            cylinder(r=100, h=self.shield_length_mm, center=True, segments=30)
        )

        complete_shield_assembly = difference()(
            union()(hollow_shield_jacket, mounting_bracket_left, mounting_bracket_right),
            bolt_hole_left,
            bolt_hole_right
        )
        
        output_path = os.path.join(self.output_dir, "lockheed_armored_shield.scad")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"// --- UNIVAC IX AUTOMATED LOCKHEED SHIELDING bluePrints ---\n")
            f.write(f"// Target Resonant Frequency: {self.frequency} Hz\n")
            f.write(f"// Complete Shield Length   : {self.shield_length_mm:.4f} mm\n")
            f.write(scad_render(complete_shield_assembly))
            
        return output_path

if __name__ == "__main__":
    generator = LockheedArmoredShieldGenerator(fundamental_frequency_hz=13.72)
    generator.compile_shield_mesh()
