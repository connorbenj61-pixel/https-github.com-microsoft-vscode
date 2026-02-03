"""
3D Quantum Visualization and Drawing System
Creates 3D representations of quantum states and circuits for visualization and 3D laser printing.

PEGI 3: Educational 3D visualization of quantum concepts
"""

import math
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class Point3D:
    """3D point representation."""
    x: float
    y: float
    z: float
    
    def distance_to(self, other: 'Point3D') -> float:
        """Calculate distance to another point."""
        return math.sqrt(
            (self.x - other.x)**2 + 
            (self.y - other.y)**2 + 
            (self.z - other.z)**2
        )
    
    def __add__(self, other: 'Point3D') -> 'Point3D':
        """Add two points."""
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Point3D') -> 'Point3D':
        """Subtract two points."""
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def scale(self, factor: float) -> 'Point3D':
        """Scale point by factor."""
        return Point3D(self.x * factor, self.y * factor, self.z * factor)
    
    def rotate_x(self, angle: float) -> 'Point3D':
        """Rotate around X axis (angle in radians)."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Point3D(
            self.x,
            self.y * cos_a - self.z * sin_a,
            self.y * sin_a + self.z * cos_a
        )
    
    def rotate_y(self, angle: float) -> 'Point3D':
        """Rotate around Y axis (angle in radians)."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Point3D(
            self.x * cos_a + self.z * sin_a,
            self.y,
            -self.x * sin_a + self.z * cos_a
        )
    
    def rotate_z(self, angle: float) -> 'Point3D':
        """Rotate around Z axis (angle in radians)."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Point3D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
            self.z
        )
    
    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert to tuple."""
        return (self.x, self.y, self.z)


@dataclass
class Line3D:
    """3D line segment."""
    start: Point3D
    end: Point3D
    
    def length(self) -> float:
        """Get line length."""
        return self.start.distance_to(self.end)
    
    def midpoint(self) -> Point3D:
        """Get midpoint of line."""
        return Point3D(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2,
            (self.start.z + self.end.z) / 2
        )
    
    def scale(self, factor: float) -> 'Line3D':
        """Scale line around midpoint."""
        mid = self.midpoint()
        new_start = mid + (self.start - mid).scale(factor)
        new_end = mid + (self.end - mid).scale(factor)
        return Line3D(new_start, new_end)


@dataclass
class Shape3D:
    """Base 3D shape."""
    vertices: List[Point3D]
    edges: List[Tuple[int, int]]  # Indices of vertices
    faces: List[List[int]] = None  # Indices of vertices forming faces
    
    def __post_init__(self):
        if self.faces is None:
            self.faces = []
    
    def scale(self, factor: float) -> 'Shape3D':
        """Scale shape."""
        return Shape3D(
            [v.scale(factor) for v in self.vertices],
            self.edges,
            self.faces
        )
    
    def rotate_x(self, angle: float) -> 'Shape3D':
        """Rotate around X axis."""
        return Shape3D(
            [v.rotate_x(angle) for v in self.vertices],
            self.edges,
            self.faces
        )
    
    def rotate_y(self, angle: float) -> 'Shape3D':
        """Rotate around Y axis."""
        return Shape3D(
            [v.rotate_y(angle) for v in self.vertices],
            self.edges,
            self.faces
        )
    
    def rotate_z(self, angle: float) -> 'Shape3D':
        """Rotate around Z axis."""
        return Shape3D(
            [v.rotate_z(angle) for v in self.vertices],
            self.edges,
            self.faces
        )
    
    def translate(self, offset: Point3D) -> 'Shape3D':
        """Translate shape."""
        return Shape3D(
            [v + offset for v in self.vertices],
            self.edges,
            self.faces
        )
    
    def get_lines(self) -> List[Line3D]:
        """Get all lines from edges."""
        return [Line3D(self.vertices[e[0]], self.vertices[e[1]]) 
                for e in self.edges]
    
    def bounding_box(self) -> Tuple[Point3D, Point3D]:
        """Get bounding box (min, max)."""
        if not self.vertices:
            return Point3D(0, 0, 0), Point3D(0, 0, 0)
        
        min_x = min(v.x for v in self.vertices)
        max_x = max(v.x for v in self.vertices)
        min_y = min(v.y for v in self.vertices)
        max_y = max(v.y for v in self.vertices)
        min_z = min(v.z for v in self.vertices)
        max_z = max(v.z for v in self.vertices)
        
        return Point3D(min_x, min_y, min_z), Point3D(max_x, max_y, max_z)


class Shape3DFactory:
    """Factory for creating common 3D shapes."""
    
    @staticmethod
    def cube(size: float = 1.0) -> Shape3D:
        """Create a cube."""
        s = size / 2
        vertices = [
            Point3D(-s, -s, -s),  # 0
            Point3D(s, -s, -s),   # 1
            Point3D(s, s, -s),    # 2
            Point3D(-s, s, -s),   # 3
            Point3D(-s, -s, s),   # 4
            Point3D(s, -s, s),    # 5
            Point3D(s, s, s),     # 6
            Point3D(-s, s, s),    # 7
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom
            (4, 5), (5, 6), (6, 7), (7, 4),  # Top
            (0, 4), (1, 5), (2, 6), (3, 7),  # Sides
        ]
        faces = [
            [0, 1, 2, 3],  # Bottom
            [4, 5, 6, 7],  # Top
            [0, 1, 5, 4],  # Front
            [2, 3, 7, 6],  # Back
            [0, 3, 7, 4],  # Left
            [1, 2, 6, 5],  # Right
        ]
        return Shape3D(vertices, edges, faces)
    
    @staticmethod
    def sphere(radius: float = 1.0, segments: int = 8) -> Shape3D:
        """Create an approximated sphere."""
        vertices = []
        edges = []
        
        # Create vertices
        for i in range(segments + 1):
            lat = math.pi * i / segments
            for j in range(segments):
                lon = 2 * math.pi * j / segments
                x = radius * math.sin(lat) * math.cos(lon)
                y = radius * math.cos(lat)
                z = radius * math.sin(lat) * math.sin(lon)
                vertices.append(Point3D(x, y, z))
        
        # Create edges
        for i in range(segments):
            for j in range(segments):
                v1 = i * segments + j
                v2 = i * segments + (j + 1) % segments
                v3 = ((i + 1) % (segments + 1)) * segments + j
                
                edges.append((v1, v2))
                edges.append((v1, v3))
        
        return Shape3D(vertices, edges, [])
    
    @staticmethod
    def pyramid(base_size: float = 1.0, height: float = 1.0) -> Shape3D:
        """Create a pyramid."""
        s = base_size / 2
        vertices = [
            Point3D(-s, 0, -s),   # 0 - base corners
            Point3D(s, 0, -s),    # 1
            Point3D(s, 0, s),     # 2
            Point3D(-s, 0, s),    # 3
            Point3D(0, height, 0) # 4 - apex
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Base
            (0, 4), (1, 4), (2, 4), (3, 4),  # Sides
        ]
        faces = [
            [0, 1, 2, 3],  # Base
            [0, 1, 4],     # Side 1
            [1, 2, 4],     # Side 2
            [2, 3, 4],     # Side 3
            [3, 0, 4],     # Side 4
        ]
        return Shape3D(vertices, edges, faces)
    
    @staticmethod
    def bloch_sphere() -> Shape3D:
        """Create a Bloch sphere (quantum state visualization)."""
        return Shape3DFactory.sphere(radius=1.0, segments=12)
    
    @staticmethod
    def quantum_gate_symbol(gate_type: str) -> Shape3D:
        """Create 3D representation of quantum gate."""
        if gate_type.lower() == "hadamard":
            # H-shaped structure
            vertices = [
                Point3D(-0.5, -0.5, -0.1),
                Point3D(-0.5, 0.5, -0.1),
                Point3D(-0.1, -0.1, -0.1),
                Point3D(-0.1, 0.1, -0.1),
                Point3D(0.5, -0.5, -0.1),
                Point3D(0.5, 0.5, -0.1),
            ]
            edges = [
                (0, 1), (2, 3), (4, 5),  # Vertical lines
                (1, 3), (3, 4),          # Horizontal connections
            ]
            return Shape3D(vertices, edges)
        elif gate_type.lower() == "pauli":
            # X-shaped structure
            vertices = [
                Point3D(-0.5, -0.5, 0),
                Point3D(0.5, 0.5, 0),
                Point3D(-0.5, 0.5, 0),
                Point3D(0.5, -0.5, 0),
            ]
            edges = [(0, 1), (2, 3)]
            return Shape3D(vertices, edges)
        else:
            # Default: cube
            return Shape3DFactory.cube()


class Quantum3DVisualizer:
    """Visualize quantum states and circuits in 3D."""
    
    @staticmethod
    def create_qubit_visualization(alpha_real: float, alpha_imag: float,
                                   beta_real: float, beta_imag: float) -> Shape3D:
        """Create 3D visualization of a qubit state on Bloch sphere."""
        # Create Bloch sphere
        sphere = Shape3DFactory.bloch_sphere()
        
        # Calculate state vector on Bloch sphere
        # theta = 2 * arccos(|alpha|)
        # phi = arg(beta) - arg(alpha)
        alpha_mag = math.sqrt(alpha_real**2 + alpha_imag**2)
        beta_mag = math.sqrt(beta_real**2 + beta_imag**2)
        
        theta = 2 * math.acos(max(0, min(1, alpha_mag)))
        
        if beta_mag > 1e-10:
            alpha_angle = math.atan2(alpha_imag, alpha_real)
            beta_angle = math.atan2(beta_imag, beta_real)
            phi = beta_angle - alpha_angle
        else:
            phi = 0
        
        # State vector position on sphere
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)
        
        # Arrow from origin to state
        arrow_start = Point3D(0, 0, 0)
        arrow_end = Point3D(x, y, z)
        
        return sphere
    
    @staticmethod
    def create_quantum_circuit_3d(num_qubits: int) -> Shape3D:
        """Create 3D visualization of quantum circuit."""
        vertices = []
        edges = []
        
        # Create vertical lines for each qubit
        for i in range(num_qubits):
            y_pos = -num_qubits / 2 + i
            start = Point3D(-5, y_pos, 0)
            end = Point3D(5, y_pos, 0)
            vertices.extend([start, end])
            edges.append((len(vertices) - 2, len(vertices) - 1))
        
        # Add gate boxes (simplified)
        for i in range(num_qubits):
            y_pos = -num_qubits / 2 + i
            gate_box = Shape3DFactory.cube(0.3).translate(Point3D(0, y_pos, 0))
            vertices.extend(gate_box.vertices)
        
        return Shape3D(vertices, edges, [])
    
    @staticmethod
    def create_entanglement_visualization() -> Shape3D:
        """Create 3D visualization of entangled qubits."""
        # Two spheres connected by lines
        sphere1 = Shape3DFactory.sphere(0.5).translate(Point3D(-2, 0, 0))
        sphere2 = Shape3DFactory.sphere(0.5).translate(Point3D(2, 0, 0))
        
        # Combine
        vertices = sphere1.vertices + sphere2.vertices
        edges = sphere1.edges + [(e[0], e[1]) for e in sphere2.edges]
        
        # Add connection lines
        offset = len(sphere1.vertices)
        edges.append((len(sphere1.vertices) // 2, offset + len(sphere2.vertices) // 2))
        
        return Shape3D(vertices, edges, [])


class CADExporter:
    """Export 3D shapes to CAD-friendly formats."""
    
    @staticmethod
    def to_scad(shape: Shape3D, filename: str) -> str:
        """Generate OpenSCAD code for 3D shape."""
        scad_code = "// OpenSCAD 3D Model\n"
        scad_code += "// Generated by Quantum3DVisualizer\n\n"
        
        # Create polyhedron from vertices and faces
        if shape.faces:
            scad_code += "vertices = [\n"
            for v in shape.vertices:
                scad_code += f"  [{v.x:.3f}, {v.y:.3f}, {v.z:.3f}],\n"
            scad_code += "];\n\n"
            
            scad_code += "faces = [\n"
            for face in shape.faces:
                scad_code += f"  {face},\n"
            scad_code += "];\n\n"
            
            scad_code += "polyhedron(points=vertices, faces=faces);\n"
        else:
            # Use edges to draw lines
            scad_code += "// Lines representation\n"
            for start_idx, end_idx in shape.edges:
                v1 = shape.vertices[start_idx]
                v2 = shape.vertices[end_idx]
                mid = Point3D(
                    (v1.x + v2.x) / 2,
                    (v1.y + v2.y) / 2,
                    (v1.z + v2.z) / 2
                )
                length = v1.distance_to(v2)
                scad_code += f"// Line from ({v1.x:.3f}, {v1.y:.3f}, {v1.z:.3f}) "
                scad_code += f"to ({v2.x:.3f}, {v2.y:.3f}, {v2.z:.3f})\n"
        
        return scad_code
    
    @staticmethod
    def to_stl_text(shape: Shape3D) -> str:
        """Generate STL text format (ASCII STL)."""
        stl_data = "solid quantum_shape\n"
        
        # Export faces as triangles
        if shape.faces:
            for face in shape.faces:
                if len(face) >= 3:
                    # Export first triangle of face
                    v1 = shape.vertices[face[0]]
                    v2 = shape.vertices[face[1]]
                    v3 = shape.vertices[face[2]]
                    
                    # Calculate normal (simplified)
                    edge1 = v2 - v1
                    edge2 = v3 - v1
                    normal_x = edge1.y * edge2.z - edge1.z * edge2.y
                    normal_y = edge1.z * edge2.x - edge1.x * edge2.z
                    normal_z = edge1.x * edge2.y - edge1.y * edge2.x
                    norm_len = math.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
                    if norm_len > 0:
                        normal_x /= norm_len
                        normal_y /= norm_len
                        normal_z /= norm_len
                    
                    stl_data += f"  facet normal {normal_x:.6f} {normal_y:.6f} {normal_z:.6f}\n"
                    stl_data += "    outer loop\n"
                    stl_data += f"      vertex {v1.x:.6f} {v1.y:.6f} {v1.z:.6f}\n"
                    stl_data += f"      vertex {v2.x:.6f} {v2.y:.6f} {v2.z:.6f}\n"
                    stl_data += f"      vertex {v3.x:.6f} {v3.y:.6f} {v3.z:.6f}\n"
                    stl_data += "    endloop\n"
                    stl_data += "  endfacet\n"
        
        stl_data += "endsolid quantum_shape\n"
        return stl_data
    
    @staticmethod
    def to_obj(shape: Shape3D) -> str:
        """Generate OBJ format (Wavefront)."""
        obj_data = "# Wavefront OBJ\n"
        obj_data += "# Generated by Quantum3DVisualizer\n\n"
        
        # Vertices
        obj_data += "# Vertices\n"
        for v in shape.vertices:
            obj_data += f"v {v.x:.6f} {v.y:.6f} {v.z:.6f}\n"
        
        # Edges
        obj_data += "\n# Edges\n"
        for e in shape.edges:
            obj_data += f"l {e[0] + 1} {e[1] + 1}\n"
        
        # Faces
        if shape.faces:
            obj_data += "\n# Faces\n"
            for face in shape.faces:
                face_str = " ".join(str(i + 1) for i in face)
                obj_data += f"f {face_str}\n"
        
        return obj_data
