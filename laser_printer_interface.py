"""
3D Laser Printer Interface System
Controls and interfaces with 3D laser printing devices for quantum visualization output.

PEGI 3: Educational interface for 3D printing technology
"""

import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from quantum_3d_visualizer import Shape3D, Point3D, CADExporter


class LaserPrinterType(Enum):
    """Types of 3D laser printers."""
    STEREOLITHOGRAPHY = "SLA"  # Resin-based
    SELECTIVE_LASER_SINTERING = "SLS"  # Powder-based
    SELECTIVE_LASER_MELTING = "SLM"  # Metal-based
    DIRECT_METAL_LASER = "DMLS"  # Direct metal
    LASER_ABLATION = "LASE"  # Laser ablation
    HYBRID_LASER = "HYBRID"  # Multi-material


@dataclass
class LaserConfig:
    """Laser printer configuration."""
    printer_type: LaserPrinterType
    build_area_x: float  # mm
    build_area_y: float  # mm
    build_area_z: float  # mm
    resolution: float  # micrometers per pixel
    laser_power: float  # watts
    scan_speed: float  # mm/s
    layer_height: float  # mm
    material: str  # Material type
    
    def is_valid(self, shape: Shape3D) -> bool:
        """Check if shape fits in build area."""
        if not shape.vertices:
            return False
        
        min_pt, max_pt = shape.bounding_box()
        
        return (
            max_pt.x - min_pt.x <= self.build_area_x and
            max_pt.y - min_pt.y <= self.build_area_y and
            max_pt.z - min_pt.z <= self.build_area_z
        )


class ScanPath:
    """Represents a scan path for laser."""
    
    def __init__(self):
        self.points: List[Point3D] = []
        self.power_levels: List[float] = []
        self.speed_levels: List[float] = []
    
    def add_point(self, point: Point3D, power: float, speed: float):
        """Add point to scan path."""
        self.points.append(point)
        self.power_levels.append(power)
        self.speed_levels.append(speed)
    
    def total_distance(self) -> float:
        """Calculate total distance of scan path."""
        if len(self.points) < 2:
            return 0
        
        distance = 0
        for i in range(len(self.points) - 1):
            distance += self.points[i].distance_to(self.points[i + 1])
        
        return distance
    
    def estimated_time(self, speed_multiplier: float = 1.0) -> float:
        """Estimate print time in seconds."""
        if len(self.speed_levels) == 0:
            return 0
        
        total_time = 0
        for i in range(len(self.points) - 1):
            dist = self.points[i].distance_to(self.points[i + 1])
            speed = self.speed_levels[i] * speed_multiplier
            if speed > 0:
                total_time += dist / speed * 1000  # Convert to seconds
        
        return total_time


class ScanStrategy:
    """Different strategies for laser scanning."""
    
    @staticmethod
    def raster_scan(shape: Shape3D, config: LaserConfig, 
                   z_layer: float) -> ScanPath:
        """Raster scan strategy (back and forth lines)."""
        path = ScanPath()
        
        min_pt, max_pt = shape.bounding_box()
        
        # Scan in X direction with Y stepping
        y = min_pt.y
        x_dir = 1
        
        while y <= max_pt.y:
            if x_dir > 0:
                x_start, x_end = min_pt.x, max_pt.x
            else:
                x_start, x_end = max_pt.x, min_pt.x
            
            x = x_start
            while (x_dir > 0 and x <= x_end) or (x_dir < 0 and x >= x_end):
                point = Point3D(x, y, z_layer)
                path.add_point(point, config.laser_power, config.scan_speed)
                x += x_dir * config.resolution / 1000  # Convert micrometers to mm
            
            y += config.layer_height
            x_dir *= -1  # Reverse direction for next line
        
        return path
    
    @staticmethod
    def spiral_scan(shape: Shape3D, config: LaserConfig,
                   z_layer: float) -> ScanPath:
        """Spiral scan strategy (outward spiral)."""
        path = ScanPath()
        
        center_x = (shape.vertices[0].x + shape.vertices[-1].x) / 2 if shape.vertices else 0
        center_y = (shape.vertices[0].y + shape.vertices[-1].y) / 2 if shape.vertices else 0
        
        radius = 0.1
        max_radius = 5.0
        angle_step = math.pi / 180  # 1 degree steps
        radius_step = 0.01
        
        angle = 0
        while radius < max_radius:
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            point = Point3D(x, y, z_layer)
            path.add_point(point, config.laser_power, config.scan_speed)
            
            angle += angle_step
            radius += radius_step
        
        return path
    
    @staticmethod
    def vector_scan(shape: Shape3D, config: LaserConfig,
                   z_layer: float) -> ScanPath:
        """Vector scan following shape edges."""
        path = ScanPath()
        
        for edge in shape.edges:
            start = shape.vertices[edge[0]]
            end = shape.vertices[edge[1]]
            
            # Sample points along edge
            distance = start.distance_to(end)
            num_points = int(distance * 1000 / config.resolution)
            
            for i in range(num_points):
                t = i / max(1, num_points - 1)
                x = start.x + (end.x - start.x) * t
                y = start.y + (end.y - start.y) * t
                point = Point3D(x, y, z_layer)
                path.add_point(point, config.laser_power * 0.8, config.scan_speed * 1.2)
        
        return path


class LaserPrintJob:
    """Represents a 3D laser print job."""
    
    def __init__(self, shape: Shape3D, config: LaserConfig, 
                 strategy: str = "raster"):
        self.shape = shape
        self.config = config
        self.strategy = strategy
        self.scan_paths: List[ScanPath] = []
        self.material_used: float = 0.0  # grams
        self.status = "CREATED"
        self.progress: float = 0.0
    
    def prepare(self) -> bool:
        """Prepare print job."""
        if not self.config.is_valid(self.shape):
            return False
        
        # Generate scan paths for each layer
        min_pt, max_pt = self.shape.bounding_box()
        z = min_pt.z
        
        while z <= max_pt.z:
            if self.strategy == "raster":
                path = ScanStrategy.raster_scan(self.shape, self.config, z)
            elif self.strategy == "spiral":
                path = ScanStrategy.spiral_scan(self.shape, self.config, z)
            elif self.strategy == "vector":
                path = ScanStrategy.vector_scan(self.shape, self.config, z)
            else:
                path = ScanStrategy.raster_scan(self.shape, self.config, z)
            
            self.scan_paths.append(path)
            z += self.config.layer_height
        
        self.status = "PREPARED"
        return True
    
    def calculate_material(self) -> float:
        """Calculate material needed (grams)."""
        min_pt, max_pt = self.shape.bounding_box()
        
        volume = (
            (max_pt.x - min_pt.x) * 
            (max_pt.y - min_pt.y) * 
            (max_pt.z - min_pt.z)
        )
        
        # Density depends on material (simplified)
        densities = {
            "resin": 1.1,  # g/cm³
            "nylon": 1.14,
            "titanium": 4.5,
            "aluminum": 2.7,
            "steel": 7.85,
            "plastic": 1.05
        }
        
        density = densities.get(self.config.material.lower(), 1.0)
        material = volume * density
        
        self.material_used = material
        return material
    
    def estimate_time(self) -> float:
        """Estimate print time in seconds."""
        total_time = 0
        for path in self.scan_paths:
            total_time += path.estimated_time()
        
        # Add overhead (setup, cooling, etc.)
        total_time += len(self.scan_paths) * 5  # 5 seconds per layer
        
        return total_time
    
    def format_time(self, seconds: float) -> str:
        """Format time as human-readable string."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    def get_job_info(self) -> Dict:
        """Get job information."""
        material = self.calculate_material()
        time = self.estimate_time()
        
        return {
            "status": self.status,
            "strategy": self.strategy,
            "num_layers": len(self.scan_paths),
            "material_needed": f"{material:.2f}g",
            "estimated_time": self.format_time(time),
            "estimated_time_seconds": time,
            "progress": f"{self.progress:.1f}%",
            "shape_bounds": {
                "min": self.shape.bounding_box()[0].to_tuple(),
                "max": self.shape.bounding_box()[1].to_tuple()
            },
            "build_area": {
                "x": self.config.build_area_x,
                "y": self.config.build_area_y,
                "z": self.config.build_area_z
            },
            "resolution": f"{self.config.resolution} micrometers",
            "laser_power": f"{self.config.laser_power}W",
            "material_type": self.config.material
        }
    
    def simulate_print(self) -> List[Dict]:
        """Simulate print process."""
        layer_results = []
        
        for i, path in enumerate(self.scan_paths):
            distance = path.total_distance()
            power_avg = sum(path.power_levels) / len(path.power_levels) if path.power_levels else 0
            
            result = {
                "layer": i + 1,
                "total_layers": len(self.scan_paths),
                "points_in_layer": len(path.points),
                "scan_distance": f"{distance:.2f}mm",
                "average_power": f"{power_avg:.1f}W",
                "estimated_layer_time": self.format_time(path.estimated_time()),
                "status": "COMPLETED"
            }
            layer_results.append(result)
            self.progress = ((i + 1) / len(self.scan_paths)) * 100
        
        self.status = "COMPLETED"
        return layer_results


class LaserPrinterController:
    """Controls 3D laser printer operations."""
    
    def __init__(self, printer_type: LaserPrinterType = LaserPrinterType.STEREOLITHOGRAPHY):
        self.printer_type = printer_type
        self.config: Optional[LaserConfig] = None
        self.current_job: Optional[LaserPrintJob] = None
        self.print_history: List[LaserPrintJob] = []
        self.is_ready = False
    
    def initialize(self, config: LaserConfig) -> bool:
        """Initialize printer with configuration."""
        self.config = config
        self.is_ready = True
        return True
    
    def create_job(self, shape: Shape3D, strategy: str = "raster") -> Optional[LaserPrintJob]:
        """Create a print job."""
        if not self.is_ready or self.config is None:
            return None
        
        job = LaserPrintJob(shape, self.config, strategy)
        return job
    
    def submit_job(self, job: LaserPrintJob) -> bool:
        """Submit job to printer."""
        if not job.prepare():
            return False
        
        self.current_job = job
        self.print_history.append(job)
        return True
    
    def get_print_status(self) -> Dict:
        """Get current print status."""
        if self.current_job is None:
            return {
                "status": "IDLE",
                "message": "No active print job"
            }
        
        return self.current_job.get_job_info()
    
    def cancel_job(self) -> bool:
        """Cancel current print job."""
        if self.current_job is None:
            return False
        
        self.current_job.status = "CANCELLED"
        self.current_job = None
        return True
    
    def export_gcode(self, job: LaserPrintJob) -> str:
        """Export job as GCode for laser printer."""
        gcode = "; Generated GCode for 3D Laser Printer\n"
        gcode += f"; Material: {job.config.material}\n"
        gcode += f"; Laser Power: {job.config.laser_power}W\n"
        gcode += f"; Scan Speed: {job.config.scan_speed}mm/s\n"
        gcode += f"; Layer Height: {job.config.layer_height}mm\n\n"
        
        gcode += "G21  ; Set units to millimeters\n"
        gcode += "G90  ; Absolute positioning\n"
        gcode += "G28  ; Home all axes\n\n"
        
        for layer_num, path in enumerate(job.scan_paths):
            gcode += f"; Layer {layer_num + 1} of {len(job.scan_paths)}\n"
            gcode += f"G0 Z{path.points[0].z if path.points else 0:.3f}\n"
            
            for i, point in enumerate(path.points):
                power = path.power_levels[i] if i < len(path.power_levels) else 0
                speed = path.speed_levels[i] if i < len(path.speed_levels) else 0
                
                gcode += f"G1 X{point.x:.3f} Y{point.y:.3f} "
                gcode += f"F{speed:.1f} ; Power: {power:.1f}W\n"
            
            gcode += f"G4 P{int(job.config.layer_height * 1000)}  ; Dwell for layer curing\n"
            gcode += "\n"
        
        gcode += "; End of print\n"
        gcode += "M104 S0  ; Turn off laser\n"
        gcode += "G28  ; Home all axes\n"
        
        return gcode
    
    def get_printer_info(self) -> Dict:
        """Get printer information."""
        if self.config is None:
            return {"status": "NOT_INITIALIZED"}
        
        return {
            "printer_type": self.printer_type.value,
            "material": self.config.material,
            "build_area": {
                "x": f"{self.config.build_area_x}mm",
                "y": f"{self.config.build_area_y}mm",
                "z": f"{self.config.build_area_z}mm"
            },
            "resolution": f"{self.config.resolution} micrometers",
            "laser_power": f"{self.config.laser_power}W",
            "scan_speed": f"{self.config.scan_speed}mm/s",
            "layer_height": f"{self.config.layer_height}mm",
            "is_ready": self.is_ready,
            "jobs_completed": len(self.print_history),
            "current_job": self.current_job is not None
        }
