__author__ = 'Janos G. Hajagos'

#    Classes for generating WaveFront mesh form 3D graphics files for visualizing data
#    in a more realistic space.

import numpy as np

class ObjGraphic(object):
    def __init__(self, group_name = None, object_name = None, smoothing = False):
        self.vertices = None
        self.faces = None
        self.vector_normals = None
        self.texture_coordinates = None
        self.group_name = group_name
        self.object_name = object_name
        self.material_object = None
        self.smoothing = smoothing

    def associate_material(self,mtl_object):
        self.material_object = mtl_object

    def add_vertices(self, list_of_vertices):
        self.vertices = np.matrix(list_of_vertices)

    def add_normal_vectors(self, list_of_normal_vector):
        self.vector_normals = np.matrix(list_of_normal_vector)

    def add_texture_coordinates(self):
        pass

    def add_face(self, vertices_indices, normal_indices=None, texture_indices=None):
        pass

    def add_only_faces(self,faces):
        self.faces = np.matrix(faces)

    def _convert_regular_quad_to_mesh(self, face):
        """Converts a quadrilateral side to Triangular face:
        [1, 2,
         3, 4]
        [[1,3,4],[2,3,4]]
        """

        if len(face) != 4:
            raise RuntimeError, ""
        return [[face[0],face[2],face[3]],[face[1],face[2],face[3]]]

class Form(object):
    object_graphic = None
    def obj_graphic(self):
        return self.object_graphic

class Cube(Form):
    def __init__(self,x,y,z,edge_length):
        """Create a geometric solid that has equal length sides"""
        self.object_graph = ObjGraphic()
        el = edge_length

        #Front face   Back face   Left face   Right face  Bottom face   Top Face
        # 4 3         6  7        4  6        3 7         1 2           6 7
        # 1 2         5  8        1  5        2 8         5 8           4 3
        self.vertices = [[x,y,z],[x+el,y,z],[x+el,y,z+el],[x,y,z+el],[x,y+el,z],[x+el,y+el,z],[x+el,y+el,z+el],[x,y+el,z+el]]
        self.faces = [[1,2,3,4],[5,8,7,6],[1,5,6,4],[2,8,7,3],[5,8,2,1],[4,3,7,6]]

        self.object_graph.add_vertices(self.vertices)
        self.object_graph.add_face(self.faces)

class MtlMaterial(object):
    def __init__(self,name):
        self.name = name
        self.ambient_color = None # Ka
        self.diffuse_color = None #Kd
        self.specular_color = None # Ks
        self.specular_coefficient = None #Ns
        self.transparent = None # d or Tr range from 0 to 1
        self.illumination = None
        self.map_ambient = None # map_Ka           # the ambient texture map
        self.map_diffuse  = None# map_Kd filename.tga           # the diffuse texture map (most of the time, it will
        # be the same as the ambient texture map)
        self.map_specular = None # map_Ks lenna.tga           # specular color texture map
        self.map_specular_highlight = None #map_Ns filename.tga      # specular highlight component
        self.map_alpha_texture = None #map_d  filename.tga      # the alpha texture map
        self.map_bump = None #map_bump filename.tga

    def set_illumination(self, illumination):
        """
        0. Color on and Ambient off
        1. Color on and Ambient on
        2. Highlight on
        3. Reflection on and Ray trace on
        4. Transparency: Glass on, Reflection: Ray trace on
        5. Reflection: Fresnel on and Ray trace on
        6. Transparency: Refraction on, Reflection: Fresnel off and Ray trace on
        7. Transparency: Refraction on, Reflection: Fresnel on and Ray trace on
        8. Reflection on and Ray trace off
        9. Transparency: Glass on, Reflection: Ray trace off
        10. Casts shadows onto invisible surfaces

        Source: http://en.wikipedia.org/wiki/Wavefront_.obj_file
        """

        self.illumination = illumination



#mtllib [external .mtl file name]
#This tag specifies the material name for the element following it. The material name matches a named material definition in an external .mtl file.
#usemtl [material name]
#"""
#
#"""
#Vertex only: f v1 v2 v3 v4 ...
#Vertex/texture-coordinate:   f v1/vt1 v2/vt2 v3/vt3 ...
#Vertex/texture-coorinate normal/normal: f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3
#Vertex/normal:
#
#Named objects and polygon groups are specified via the following tags.
#o [object name]
#g [group name]


class WaveFrontFileWriter(object):
    def header(self):
        return ""
    def generate_file(self,file_object):
        pass


class ObjGraphicFileWriter(WaveFrontFileWriter):
    """Takes multiple objects and writes them to a single OBJ file taking into account
    bookkeeping for vertices, triangulation if requested, and material file association
    """
    def __init__(self,list_of_objects):
        self.list_of_objects = list_of_objects

    def generate_file(self, file_object):
        f = file_object

    def header(self):
        return ""

class MtlFileWriter(WaveFrontFileWriter):
    """Takes multiple MtlFile objects and creates a single MTL File"""

    def __init__(self,list_of_mtls):
        self.list_of_mtls = list_of_mtls
    def generate_file(self,file_object):
        f = file_object

