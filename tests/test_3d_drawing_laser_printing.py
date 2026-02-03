"""
Test suite for 3D drawing and laser printer interface capabilities.
"""

import unittest
import math
from quantum_3d_visualizer import (
    Point3D, Line3D, Shape3D, Shape3DFactory, Quantum3DVisualizer, CADExporter
)
from laser_printer_interface import (
    LaserConfig, ScanPath, ScanStrategy, LaserPrintJob, LaserPrinterController,
    LaserPrinterType
)
from armourbound_guardian import ArmourboundGuardianAI


class TestPoint3D(unittest.TestCase):
    """Test 3D point operations."""
    
    def test_point_creation(self):
        """Test creating 3D points."""
        p = Point3D(1, 2, 3)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.z, 3)
    
    def test_distance_calculation(self):
        """Test distance between points."""
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(3, 4, 0)
        self.assertAlmostEqual(p1.distance_to(p2), 5.0)
    
    def test_point_addition(self):
        """Test adding points."""
        p1 = Point3D(1, 2, 3)
        p2 = Point3D(4, 5, 6)
        p3 = p1 + p2
        self.assertEqual(p3.x, 5)
        self.assertEqual(p3.y, 7)
        self.assertEqual(p3.z, 9)
    
    def test_point_scaling(self):
        """Test scaling points."""
        p = Point3D(1, 2, 3)
        p_scaled = p.scale(2)
        self.assertEqual(p_scaled.x, 2)
        self.assertEqual(p_scaled.y, 4)
        self.assertEqual(p_scaled.z, 6)
    
    def test_rotation_x(self):
        """Test rotation around X axis."""
        p = Point3D(0, 1, 0)
        p_rot = p.rotate_x(math.pi / 2)
        self.assertAlmostEqual(p_rot.y, 0, places=5)
        self.assertAlmostEqual(p_rot.z, 1, places=5)


class TestLine3D(unittest.TestCase):
    """Test 3D line operations."""
    
    def test_line_length(self):
        """Test calculating line length."""
        line = Line3D(Point3D(0, 0, 0), Point3D(3, 4, 0))
        self.assertAlmostEqual(line.length(), 5.0)
    
    def test_midpoint(self):
        """Test finding midpoint."""
        line = Line3D(Point3D(0, 0, 0), Point3D(4, 4, 4))
        mid = line.midpoint()
        self.assertEqual(mid.x, 2)
        self.assertEqual(mid.y, 2)
        self.assertEqual(mid.z, 2)


class TestShape3DFactory(unittest.TestCase):
    """Test creating 3D shapes."""
    
    def test_cube_creation(self):
        """Test creating a cube."""
        cube = Shape3DFactory.cube(1.0)
        self.assertEqual(len(cube.vertices), 8)
        self.assertEqual(len(cube.edges), 12)
        self.assertEqual(len(cube.faces), 6)
    
    def test_sphere_creation(self):
        """Test creating a sphere."""
        sphere = Shape3DFactory.sphere(1.0, segments=8)
        self.assertGreater(len(sphere.vertices), 0)
        self.assertGreater(len(sphere.edges), 0)
    
    def test_pyramid_creation(self):
        """Test creating a pyramid."""
        pyramid = Shape3DFactory.pyramid(1.0, 1.0)
        self.assertEqual(len(pyramid.vertices), 5)
        self.assertEqual(len(pyramid.edges), 8)
        self.assertEqual(len(pyramid.faces), 5)
    
    def test_bloch_sphere(self):
        """Test creating Bloch sphere."""
        sphere = Shape3DFactory.bloch_sphere()
        self.assertGreater(len(sphere.vertices), 0)
        self.assertGreater(len(sphere.edges), 0)


class TestQuantum3DVisualizer(unittest.TestCase):
    """Test quantum 3D visualization."""
    
    def test_qubit_visualization(self):
        """Test qubit on Bloch sphere."""
        sphere = Quantum3DVisualizer.create_qubit_visualization(1, 0, 0, 0)
        self.assertGreater(len(sphere.vertices), 0)
    
    def test_quantum_circuit_3d(self):
        """Test quantum circuit visualization."""
        circuit = Quantum3DVisualizer.create_quantum_circuit_3d(3)
        self.assertGreater(len(circuit.vertices), 0)
    
    def test_entanglement_visualization(self):
        """Test entanglement visualization."""
        viz = Quantum3DVisualizer.create_entanglement_visualization()
        self.assertGreater(len(viz.vertices), 0)


class TestCADExporter(unittest.TestCase):
    """Test CAD export formats."""
    
    def setUp(self):
        """Set up test shape."""
        self.shape = Shape3DFactory.cube(10.0)
    
    def test_scad_export(self):
        """Test OpenSCAD export."""
        scad = CADExporter.to_scad(self.shape, "test.scad")
        self.assertIn("polyhedron", scad)
        self.assertIn("vertices", scad)
    
    def test_stl_export(self):
        """Test STL export."""
        stl = CADExporter.to_stl_text(self.shape)
        self.assertIn("solid quantum_shape", stl)
        self.assertIn("facet normal", stl)
        self.assertIn("endsolid", stl)
    
    def test_obj_export(self):
        """Test OBJ export."""
        obj = CADExporter.to_obj(self.shape)
        self.assertIn("v ", obj)
        self.assertIn("l ", obj) or self.assertIn("f ", obj)


class TestScanPath(unittest.TestCase):
    """Test laser scan path."""
    
    def test_scan_path_creation(self):
        """Test creating scan path."""
        path = ScanPath()
        path.add_point(Point3D(0, 0, 0), 10.0, 500.0)
        path.add_point(Point3D(1, 0, 0), 10.0, 500.0)
        
        self.assertEqual(len(path.points), 2)
    
    def test_total_distance(self):
        """Test calculating path distance."""
        path = ScanPath()
        path.add_point(Point3D(0, 0, 0), 10.0, 500.0)
        path.add_point(Point3D(3, 4, 0), 10.0, 500.0)
        
        self.assertAlmostEqual(path.total_distance(), 5.0)


class TestScanStrategy(unittest.TestCase):
    """Test laser scan strategies."""
    
    def setUp(self):
        """Set up test shape and config."""
        self.shape = Shape3DFactory.cube(10.0)
        self.config = LaserConfig(
            printer_type=LaserPrinterType.STEREOLITHOGRAPHY,
            build_area_x=100.0,
            build_area_y=100.0,
            build_area_z=150.0,
            resolution=25.0,
            laser_power=10.0,
            scan_speed=500.0,
            layer_height=0.05,
            material="resin"
        )
    
    def test_raster_scan(self):
        """Test raster scan strategy."""
        path = ScanStrategy.raster_scan(self.shape, self.config, 0)
        self.assertGreater(len(path.points), 0)
    
    def test_spiral_scan(self):
        """Test spiral scan strategy."""
        path = ScanStrategy.spiral_scan(self.shape, self.config, 0)
        self.assertGreater(len(path.points), 0)
    
    def test_vector_scan(self):
        """Test vector scan strategy."""
        path = ScanStrategy.vector_scan(self.shape, self.config, 0)
        self.assertGreater(len(path.points), 0)


class TestLaserPrintJob(unittest.TestCase):
    """Test laser print job management."""
    
    def setUp(self):
        """Set up test job."""
        self.shape = Shape3DFactory.cube(15.0)
        self.config = LaserConfig(
            printer_type=LaserPrinterType.STEREOLITHOGRAPHY,
            build_area_x=100.0,
            build_area_y=100.0,
            build_area_z=150.0,
            resolution=25.0,
            laser_power=10.0,
            scan_speed=500.0,
            layer_height=0.05,
            material="resin"
        )
        self.job = LaserPrintJob(self.shape, self.config)
    
    def test_job_preparation(self):
        """Test preparing print job."""
        result = self.job.prepare()
        self.assertTrue(result)
        self.assertEqual(self.job.status, "PREPARED")
    
    def test_material_calculation(self):
        """Test material usage calculation."""
        material = self.job.calculate_material()
        self.assertGreater(material, 0)
    
    def test_time_estimation(self):
        """Test print time estimation."""
        self.job.prepare()
        time = self.job.estimate_time()
        self.assertGreater(time, 0)
    
    def test_job_info(self):
        """Test getting job information."""
        self.job.prepare()
        info = self.job.get_job_info()
        self.assertIn("status", info)
        self.assertIn("material_needed", info)
        self.assertIn("estimated_time", info)
    
    def test_print_simulation(self):
        """Test simulating print."""
        self.job.prepare()
        results = self.job.simulate_print()
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["status"], "COMPLETED")


class TestLaserPrinterController(unittest.TestCase):
    """Test laser printer controller."""
    
    def setUp(self):
        """Set up printer controller."""
        self.controller = LaserPrinterController(LaserPrinterType.STEREOLITHOGRAPHY)
        self.config = LaserConfig(
            printer_type=LaserPrinterType.STEREOLITHOGRAPHY,
            build_area_x=100.0,
            build_area_y=100.0,
            build_area_z=150.0,
            resolution=25.0,
            laser_power=10.0,
            scan_speed=500.0,
            layer_height=0.05,
            material="resin"
        )
    
    def test_initialization(self):
        """Test printer initialization."""
        result = self.controller.initialize(self.config)
        self.assertTrue(result)
        self.assertTrue(self.controller.is_ready)
    
    def test_job_creation(self):
        """Test creating print job."""
        self.controller.initialize(self.config)
        shape = Shape3DFactory.cube(15.0)
        job = self.controller.create_job(shape)
        self.assertIsNotNone(job)
    
    def test_job_submission(self):
        """Test submitting print job."""
        self.controller.initialize(self.config)
        shape = Shape3DFactory.cube(15.0)
        job = self.controller.create_job(shape)
        result = self.controller.submit_job(job)
        self.assertTrue(result)
    
    def test_printer_info(self):
        """Test getting printer information."""
        self.controller.initialize(self.config)
        info = self.controller.get_printer_info()
        self.assertIn("printer_type", info)
        self.assertTrue(info["is_ready"])
    
    def test_gcode_export(self):
        """Test exporting GCode."""
        self.controller.initialize(self.config)
        shape = Shape3DFactory.cube(15.0)
        job = self.controller.create_job(shape)
        self.controller.submit_job(job)
        gcode = self.controller.export_gcode(job)
        self.assertIn("G21", gcode)
        self.assertIn("G90", gcode)


class TestGuardian3DDrawing(unittest.TestCase):
    """Test Guardian AI 3D drawing capabilities."""
    
    def setUp(self):
        """Set up Guardian."""
        self.guardian = ArmourboundGuardianAI()
    
    def test_draw_3d_cube(self):
        """Test drawing cube."""
        result = self.guardian.draw_3d_shape("cube", 10.0)
        self.assertIn("shape_type", result)
        self.assertIn("vertices_count", result)
        self.assertGreater(result["vertices_count"], 0)
    
    def test_draw_3d_sphere(self):
        """Test drawing sphere."""
        result = self.guardian.draw_3d_shape("sphere", 10.0)
        self.assertIn("shape_type", result)
        self.assertGreater(result["vertices_count"], 0)
    
    def test_draw_3d_pyramid(self):
        """Test drawing pyramid."""
        result = self.guardian.draw_3d_shape("pyramid", 10.0)
        self.assertIn("shape_type", result)
        self.assertEqual(result["vertices_count"], 5)
    
    def test_draw_quantum_state_3d(self):
        """Test drawing quantum state on Bloch sphere."""
        result = self.guardian.draw_quantum_state_3d(1, 0, 0, 0)
        self.assertIn("visualization", result)
        self.assertEqual(result["visualization"], "Bloch Sphere")
    
    def test_draw_quantum_circuit_3d(self):
        """Test drawing quantum circuit."""
        result = self.guardian.draw_quantum_circuit_3d(3)
        self.assertIn("visualization", result)
        self.assertEqual(result["num_qubits"], 3)
    
    def test_draw_entanglement_3d(self):
        """Test drawing entanglement."""
        result = self.guardian.draw_entanglement_3d()
        self.assertIn("visualization", result)
        self.assertEqual(result["spheres"], 2)


class TestGuardianCADExport(unittest.TestCase):
    """Test Guardian CAD export capabilities."""
    
    def setUp(self):
        """Set up Guardian."""
        self.guardian = ArmourboundGuardianAI()
    
    def test_export_to_scad(self):
        """Test exporting to OpenSCAD."""
        result = self.guardian.export_shape_to_cad("cube", "scad")
        self.assertEqual(result["file_extension"], "scad")
        self.assertGreater(result["content_length"], 0)
    
    def test_export_to_stl(self):
        """Test exporting to STL."""
        result = self.guardian.export_shape_to_cad("cube", "stl")
        self.assertEqual(result["file_extension"], "stl")
        self.assertGreater(result["content_length"], 0)
    
    def test_export_to_obj(self):
        """Test exporting to OBJ."""
        result = self.guardian.export_shape_to_cad("cube", "obj")
        self.assertEqual(result["file_extension"], "obj")
        self.assertGreater(result["content_length"], 0)


class TestGuardianLaserPrinting(unittest.TestCase):
    """Test Guardian laser printing capabilities."""
    
    def setUp(self):
        """Set up Guardian."""
        self.guardian = ArmourboundGuardianAI()
    
    def test_initialize_printer(self):
        """Test initializing laser printer."""
        result = self.guardian.initialize_laser_printer("SLA")
        self.assertEqual(result["status"], "INITIALIZED")
        self.assertTrue(result["ready"])
    
    def test_prepare_print_job(self):
        """Test preparing print job."""
        result = self.guardian.prepare_3d_print_job("cube", "raster")
        self.assertTrue(result["job_created"])
        self.assertIn("num_layers", result)
    
    def test_simulate_3d_print(self):
        """Test simulating 3D print."""
        result = self.guardian.simulate_3d_print("cube")
        self.assertEqual(result["simulation"], "COMPLETED")
        self.assertGreater(result["total_layers"], 0)
    
    def test_export_gcode(self):
        """Test exporting GCode."""
        result = self.guardian.export_print_to_gcode("cube")
        self.assertEqual(result["export_format"], "GCode")
        self.assertGreater(result["gcode_lines"], 0)


if __name__ == "__main__":
    unittest.main()
