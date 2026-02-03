#!/usr/bin/env python3
"""Validation script for 3D drawing and laser printer implementation."""

import sys
import os

# Add workspace to path
sys.path.insert(0, os.getcwd())

def validate():
    """Validate all 3D drawing and laser printer modules."""
    print("=" * 60)
    print("VALIDATION: 3D Drawing & Laser Printer Implementation")
    print("=" * 60)
    
    errors = []
    successes = []
    
    # Test 1: Import quantum_3d_visualizer
    try:
        from quantum_3d_visualizer import (
            Point3D, Line3D, Shape3D, Shape3DFactory,
            Quantum3DVisualizer, CADExporter
        )
        successes.append("✓ quantum_3d_visualizer imports successful")
        
        # Test Point3D
        p = Point3D(1, 2, 3)
        assert p.x == 1 and p.y == 2 and p.z == 3
        successes.append("  ✓ Point3D creation works")
        
        # Test distance
        p2 = Point3D(4, 6, 8)
        dist = p.distance_to(p2)
        assert abs(dist - 8.7177...) < 0.01
        successes.append("  ✓ Point3D distance calculation works")
        
        # Test Shape3DFactory
        cube = Shape3DFactory.cube(5.0)
        assert len(cube.vertices) > 0
        successes.append("  ✓ Shape3DFactory.cube() works")
        
        sphere = Shape3DFactory.sphere(10.0, 20)
        assert len(sphere.vertices) > 0
        successes.append("  ✓ Shape3DFactory.sphere() works")
        
        bloch = Shape3DFactory.bloch_sphere(5.0)
        assert len(bloch.vertices) > 0
        successes.append("  ✓ Shape3DFactory.bloch_sphere() works")
        
        # Test Quantum3DVisualizer
        viz = Quantum3DVisualizer()
        qubit_shape = viz.create_qubit_visualization(1.0, 0.5)
        assert qubit_shape is not None
        successes.append("  ✓ Quantum3DVisualizer.create_qubit_visualization() works")
        
        circuit_shape = viz.create_quantum_circuit_3d(3)
        assert circuit_shape is not None
        successes.append("  ✓ Quantum3DVisualizer.create_quantum_circuit_3d() works")
        
        # Test CADExporter
        exporter = CADExporter(cube)
        scad = exporter.to_scad()
        assert "polyhedron" in scad
        successes.append("  ✓ CADExporter.to_scad() works")
        
        stl = exporter.to_stl_text()
        assert "facet normal" in stl
        successes.append("  ✓ CADExporter.to_stl_text() works")
        
        obj = exporter.to_obj()
        assert "v " in obj
        successes.append("  ✓ CADExporter.to_obj() works")
        
    except Exception as e:
        errors.append(f"✗ quantum_3d_visualizer validation failed: {e}")
    
    # Test 2: Import laser_printer_interface
    try:
        from laser_printer_interface import (
            LaserPrinterType, LaserConfig, ScanPath, ScanStrategy,
            LaserPrintJob, LaserPrinterController
        )
        successes.append("\n✓ laser_printer_interface imports successful")
        
        # Test LaserConfig
        config = LaserConfig(
            build_area_x=100, build_area_y=100, build_area_z=100,
            resolution=0.1, laser_power=100, scan_speed=50,
            layer_height=0.05, material="resin"
        )
        assert config.build_area_x == 100
        successes.append("  ✓ LaserConfig creation works")
        
        # Test ScanPath
        path = ScanPath([(0, 0, 0), (10, 0, 0), (10, 10, 0)])
        assert path.total_distance() > 0
        successes.append("  ✓ ScanPath.total_distance() works")
        
        # Test ScanStrategy
        raster = ScanStrategy.raster_scan([(0, 0), (10, 0), (10, 10)], 5)
        assert len(raster.points) > 0
        successes.append("  ✓ ScanStrategy.raster_scan() works")
        
        spiral = ScanStrategy.spiral_scan(5.0, 100, 50)
        assert len(spiral.points) > 0
        successes.append("  ✓ ScanStrategy.spiral_scan() works")
        
        vector = ScanStrategy.vector_scan([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        assert len(vector.points) > 0
        successes.append("  ✓ ScanStrategy.vector_scan() works")
        
        # Test LaserPrinterController
        controller = LaserPrinterController(LaserPrinterType.SLA, config)
        assert controller.printer_type == LaserPrinterType.SLA
        successes.append("  ✓ LaserPrinterController creation works")
        
        info = controller.get_printer_info()
        assert "SLA" in info
        successes.append("  ✓ LaserPrinterController.get_printer_info() works")
        
    except Exception as e:
        errors.append(f"✗ laser_printer_interface validation failed: {e}")
    
    # Test 3: Guardian AI integration
    try:
        from armourbound_guardian import ArmourboundGuardianAI
        
        guardian = ArmourboundGuardianAI()
        successes.append("\n✓ ArmourboundGuardianAI imports successful")
        
        # Test 3D drawing methods
        cube = guardian.draw_3d_shape("cube", 10.0)
        assert cube is not None
        successes.append("  ✓ draw_3d_shape() works")
        
        bloch = guardian.draw_quantum_state_3d(1, 0, 0, 0)
        assert bloch is not None
        successes.append("  ✓ draw_quantum_state_3d() works")
        
        circuit = guardian.draw_quantum_circuit_3d(3)
        assert circuit is not None
        successes.append("  ✓ draw_quantum_circuit_3d() works")
        
        ent = guardian.draw_entanglement_3d()
        assert ent is not None
        successes.append("  ✓ draw_entanglement_3d() works")
        
        # Test CAD export
        cad = guardian.export_shape_to_cad("cube", "stl")
        assert cad is not None
        successes.append("  ✓ export_shape_to_cad() works")
        
        # Test laser printer methods
        printer = guardian.initialize_laser_printer("SLA")
        assert printer is not None
        successes.append("  ✓ initialize_laser_printer() works")
        
        job = guardian.prepare_3d_print_job("cube", "raster")
        assert job is not None
        successes.append("  ✓ prepare_3d_print_job() works")
        
        sim = guardian.simulate_3d_print("cube")
        assert sim is not None
        successes.append("  ✓ simulate_3d_print() works")
        
        gcode = guardian.export_print_to_gcode("cube")
        assert gcode is not None and "G" in gcode
        successes.append("  ✓ export_print_to_gcode() works")
        
    except Exception as e:
        errors.append(f"✗ ArmourboundGuardianAI integration failed: {e}")
    
    # Print results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    for success in successes:
        print(success)
    
    if errors:
        print("\n" + "=" * 60)
        print("ERRORS")
        print("=" * 60)
        for error in errors:
            print(error)
        print("\n❌ VALIDATION FAILED")
        return 1
    else:
        print("\n" + "=" * 60)
        print("✅ ALL VALIDATIONS PASSED")
        print("=" * 60)
        print(f"\n✓ {len(successes)} validation checks completed successfully")
        print("✓ 3D drawing system is functional")
        print("✓ Laser printer interface is functional")
        print("✓ Guardian AI integration is complete")
        return 0

if __name__ == "__main__":
    exit(validate())
