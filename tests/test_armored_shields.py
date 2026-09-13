import pytest
import os
import numpy as np
from src.core.generate_armored_shields import LockheedArmoredShieldGenerator
from src.core.shield_monitor import LockheedShieldMonitor

def test_procedural_lockheed_shield_mesh_generation(tmpdir):
    generator = LockheedArmoredShieldGenerator(fundamental_frequency_hz=13.72)
    generator.output_dir = str(tmpdir)
    
    scad_output_path = generator.compile_shield_mesh()
    assert os.path.exists(scad_output_path)
    with open(scad_output_path, "r") as f:
        content = f.read()
    assert "cylinder" in content
    assert "cube" in content
    assert "difference" in content

def test_shield_acoustic_harmonic_monitoring():
    monitor = LockheedShieldMonitor(target_frequency=13.72)
    
    # Emulate sensor layout strings tracking nominal acoustic peak node positions
    mock_sensor_positions_mm = np.array([0.0, 25000.0, 50000.0], dtype=np.float32)
    
    result = monitor.process_shield_telemetry_bus(mock_sensor_positions_mm)
    
    assert result["origin"] == "LOCKHEED_SHIELD_MONITOR"
    assert result["shield_acoustic_match_efficiency"] > 0.95
    assert result["bridge_interlock_status"] == "NOMINAL_SHIELD_RESONANCE_STABLE"
    assert result["hex_voltage_state"] in ["0.EV", "0.FV"]
