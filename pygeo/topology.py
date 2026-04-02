# Standard Python modules
import sys

# External modules
import numpy as np

# Local modules
from .geo_utils.index_position import indexPosition1D, indexPosition2D, indexPosition3D
from .geo_utils.node_edge_face import (
    Edge,
    Node,
    edgeAngle,
    edgeAngleSorted,
    edgeAngleSortedInd,
    edgeMidPt,
    edgeMidPtSorted,
    edgeMidPtSortedInd,
)
from .geo_utils.remove_duplicates import pointReduce


class Topology:
    """
    Topology is a general base class that defines the connectivity
    for any n-dimensional b-spline patch. This is used by the pyGeo
    (surfaces 2D) and pyBlock (volumes 3D) modules.
    """

    def __init__(self):
        self.nNode = None
        self.nEdge = None
        self.nFace = None
        self.nGlobal = None
        self.mNodeEnt = None
        self.mEdgeEnt = None
        self.mFaceEnt = None
        self.nodeLink = None
        self.edgeLink = None
        self.faceLink = None
        self.edgeDir = None
        self.faceDir = None
        self.lIndex = None
        self.gIndex = None
        self.edges = None
        self.simple = None
        self.topoType = None
        self.periodic = None
        self.nDG = None

    def _calcDGs(self, edges, edgeLink, edgeLinkSorted, edgeLinkInd):
        dgCounter = -1
        for i in range(self.nEdge):
            if edges[i][2] == -1:  # Not set yet
                dgCounter += 1
                edges[i][2] = dgCounter
                self._addDGEdge(i, edges, edgeLink, edgeLinkSorted, edgeLinkInd)

        self.nDG = dgCounter + 1

    def _addDGEdge(self, i, edges, edgeLink, edgeLinkSorted, edgeLinkInd):